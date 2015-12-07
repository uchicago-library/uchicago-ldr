
__author__ = "Tyler Danstrom"
__copyright__ = "Copyright 2015, The University of Chicago"
__version__ = "1.0.0"
__maintainer__ = "Tyler Danstrom"
__email__ = "tdanstrom@uchicago.edu"
__status__ = "Production"
__description__ = "This program takes a random selection of files from the ldr database and evaluates for file corruption."

from sys import argv, path

from argparse import Action, ArgumentParser
from configobj import ConfigObj
from datetime import datetime, timedelta
from grp import getgrgid
from pwd import getpwuid
from hashlib import md5, sha256
from logging import DEBUG, FileHandler, Formatter, getLogger, \
    INFO, StreamHandler
from os import _exit, stat
from os.path import basename, exists, join, relpath
from re import compile as re_compile, split as re_split
from sqlalchemy import Table
from sys import stdout
from xml.etree import ElementTree as ET

from uchicagoldr.batch import Batch
from uchicagoldr.database import Database
from uchicagoldrsips.LDRFileTree import Data
from uchicagoldrsips.SIPS import Aggregation, BaseNamespace, DateValue, IntegerValue, \
    LDRURL, Namespace, PIURL, Proxy, ProvidedCHO, RDFSResource, ResourceMap, RightsURL, \
    Statement, SubjectURL, TextValue, Triple, URL, Value, WebResource
from uchicagoldrsips.campub import campub_providedcho, campub_rem, campub_proxy

def evaluate_items(b, createdate):
    for n in b.items:
        header_pat = re_compile('^(\d{4}-\d{3})')
        if exists(n.filepath):
            n.root_path = args.root
            accession = n.find_file_accession()
            n.set_accession(accession)
            canonpath = n.find_canonical_filepath()
            if header_pat.search(canonpath):
                dirheader = header_pat.search(canonpath).group(1)
                canonpath = '/'.join(canonpath.split('/')[1:])
            else:
                dirheader = ""
                canonpath = canonpath
            n.set_canonical_filepath(canonpath)
            n.dirhead = dirheader
            n.createdate = createdate
            sha256_fixity = n.find_hash_of_file(sha256)
            md5_fixity = n.find_hash_of_file(md5)
            n.checksum = sha256_fixity
            mime = n.find_file_mime_type()
            size = n.find_file_size()
            n.mimetype = mime
            n.file_size = size
            accession = n.find_file_accession()
            if n.filepath.endswith('.dc.xml'):
                opened_file = open(n.filepath,'r')
                xml_doc = ET.parse(opened_file)
                xml_root = xml_doc.getroot()
                n.title = xml_root.find('title').text if xml_root.find('title') != None else ""
                n.description = xml_root.find('description').text \
                                if xml_root.find('description') != None else ""
                n.date = xml_root.find('date').text if xml_root.find('date') != None else ""
                n.identifier = xml_root.find('identifier').text if xml_root.find('identiifer') != None else ""
            if n.mimetype == 'image/tiff':
                fits_file_path = join(n.filepath+'.fits.xml')
                if exists(fits_file_path):
                    opened_file = open(join(n.filepath+'.fits.xml'),'r')
                    xml_doc = ET.parse(opened_file)
                    xml_root = xml_doc.getroot()
                    md5checksum = xml_root.find("{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fileinfo/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}md5checksum")
                    imageheight = xml_root.find("{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageHeight")
                    imagewidth = xml_root.find("{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}imageWidth")
                    bitspersample =  xml_root.find("{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}metadata/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}image/" + \
                                                "{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}bitsPerSample")
                    n.imageheight = imageheight.text if imageheight != None else ""
                    n.imagewidth = imagewidth.text if imagewidth != None else ""
                    n.bitspersample = bitspersample.text if bitspersample != None else ""
                    n.mixchecksum = md5checksum.text if md5checksum != None else ""
                else:
                    logger.error("no fits.xml file for tiff {filename}". \
                                 format(filename = n.filepath))
            yield n
        else:
            logger.error("{path} does not exist on the filesystem". \
                         format(path=n.filepath))            

def main():
    parser = ArgumentParser(description="{description}". \
                            format(description=__description__),
                            epilog="Copyright University of Chicago; " + \
                            "written by {author} ". \
                            format(author = __author__) + \
                            " <{email}> University of Chicago". \
                            format(email = __email__))
    parser.add_argument("-v", help="See the version of this program",
                        action="version", version=__version__)
    parser.add_argument( \
                         '-b','-verbose',help="set verbose logging",
                         action='store_const',dest='log_level',
                         const=INFO \
    )
    parser.add_argument( \
                         '-d','--debugging',help="set debugging logging",
                         action='store_const',dest='log_level',
                         const=DEBUG \
    )
    parser.add_argument( \
                         '-l','--log_loc',help="save logging to a file",
                         action="store_const",dest="log_loc",
                         const='./{progname}.log'. \
                         format(progname=argv[0]) \
    )
    parser.add_argument("-o","--object_level",
                        help="Enter the level at which object starts",
                        type=int,
                        action='store')
    parser.add_argument("-r", "--root",
                       help="Enter the root of the directory path",
                        action="store")
    parser.add_argument("directory_path", 
                        help="Enter a directory that you need to work on ",
                        action='store')

    parser.add_argument('pattern', help="Enter a pattern to filter files with",
                        action="store")
    global args
    args = parser.parse_args()
    log_format = Formatter( \
                            "[%(levelname)s] %(asctime)s  " + \
                            "= %(message)s",
                            datefmt="%Y-%m-%dT%H:%M:%S" \
    )
    global logger
    logger = getLogger( \
                        "lib.uchicago.repository.logger" \
    )
    ch = StreamHandler()
    ch.setFormatter(log_format)
    try:
        logger.setLevel(args.log_level)
    except TypeError:
        logger.setLevel(INFO)
    if args.log_loc:
        fh = FileHandler(args.log_loc)
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    logger.addHandler(ch)
    current_date = datetime.now()
    isof_current_date = current_date.strftime("%Y-%m-%dT%H:%M:%S")
    sixty_days_ago_date = current_date - timedelta(days=60)
    isof_sixty_days_ago_date = sixty_days_ago_date.strftime( \
                            "%Y-%m-%dT%H:%M:%S")
    db = Database("sqlite:////media/repo/repository/databases/" +  
                  "official/repositoryAccessions.db.new",tables_to_bind= \
                  ['record'])

    class Record(db.base):
        __table__ = Table('record', db.metadata, autoload=True)

    b = Batch(args.root, directory = args.directory_path)
    difference_in_path = relpath(args.directory_path, args.root)
    query = db.session.query(Record.createdate).filter(Record.receipt == \
                                                       difference_in_path) 
    createdate = query.first()[0]
    items = b.find_items(from_directory = True, 
                         filterable = re_compile(args.pattern))
    b.set_items(items)

    try:
        generated_data = evaluate_items(b,createdate)
        objects = {}
        descriptive_metadata = '.dc.xml$'
        representation_file = '.pdf$'
        mets_file = '.mets.xml$'
        file_definers = ['dc.xml','ALTO','TIFF','JPEG','pdf','mets.xml']
        file_definer_sequences = ['ALTO','TIFF','JPEG']
        page_number_pattern = '_(\w{4})'
        edmns = Namespace("edm", "http://www.europeana.eu/schemas/edm/")
        dcns = Namespace("dc", "http://purl.org/dc/elements/1.1/")
        dctermsns = Namespace("dcterms", "http://purl.org/dc/terms/")
        ercns = Namespace("erc", "http://purl.org/kernel/elements/1.1/")
        foafns = Namespace("foaf", "http://xmlns.com/foaf/0.1/")
        ldrns = Namespace("ldr", "http://repository.lib.uchicago.edu/ldr/")
        mixns = Namespace("mix", "http://www.loc.gov/mix/v20")
        oains = Namespace("oai", "http;//www.openarchives.org/OAI/2.0/")
        orens = Namespace("ore", "http://www.openarchives.org/ore/terms/")
        premisns = Namespace("premis", "info:lc/xmlns/premis-v2")
        rdfsns = Namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        rdfns = Namespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
        skosns = Namespace("skos", "http://www.w3.org/2004/02/skos/core#")
        xsdns = Namespace("xsd", "http://www.w3.org/2001/XMLSchema#")
        basens = BaseNamespace("http://ark.lib.uchicago.edu/ark:/61001/")
        stdout.write(str(edmns))
        stdout.write(str(dcns))
        stdout.write(str(dctermsns))
        stdout.write(str(ercns))
        stdout.write(str(foafns))
        stdout.write(str(ldrns))
        stdout.write(str(mixns))
        stdout.write(str(oains))
        stdout.write(str(orens))
        stdout.write(str(premisns))
        stdout.write(str(rdfsns))
        stdout.write(str(rdfns))
        stdout.write(str(skosns))
        stdout.write(str(xsdns))
        stdout.write(str(basens))
        for n in generated_data:
            id_parts = args.pattern.split('/')
            id_parts_enumerated = [x for x in range(args.object_level)]
            id_part_values = [n.canonical_filepath.split('/')[x] \
                              for x in id_parts_enumerated]
        
            identifier = "-".join(id_part_values)
            to_add = None
            for p in file_definers:
                if p in n.canonical_filepath:
                    to_add = n
                    break
            if to_add:
                if objects.get(identifier):
                    objects.get(identifier).append(n)
                else:
                    objects[identifier] = [n]
            else:
                logger.error("{fpath} in {id} could not be matched". \
                             format(fpath = n.canonical_filepath,
                                    id = identifier))
        logger.info("object list construction completed")
        for k, v in objects.items():
            for p in file_definer_sequences:
                sequence = sorted([(int(re_compile(page_number_pattern). \
                            search(x.canonical_filepath).group(1).lstrip('0')),
                             x.canonical_filepath) \
                            for x in v if p in x.canonical_filepath])
                known_complete_page_range = [x for x in \
                                             range(sequence[-1][0])][1:]
                what_is_actually_present  = [x[0] for x in sequence]
                if set(known_complete_page_range) - \
                   set(what_is_actually_present):
                    difference = list(set(known_complete_page_range) - \
                                      set(what_is_actually_present))
                    l = [str(x) for x in list(difference)]
                    logger.error("The sequence part {part} ". \
                                 format(part = p) + 
                                 "is missing pages {pages}". \
                                 format(pages = ','.join(l)))
            for p in file_definers:
                seek = [x for x in v if p in x.canonical_filepath]
                if len(seek) == 0:
                    logger.error("{identifier}". \
                                 format(identifier = k) + \
                                " missing part {part}".format(part = p))
        logger.info("validation completed")
        for k,v in objects.items():
            logger.info("starting {id}".format(id = k))
            identifier = k
            directory = '/'.join(identifier.split('-'))
            dcfile = [x for x in v if re_compile('.dc.xml$').search(x.canonical_filepath)][0]
            logger.info(dir(dcfile))
            logger.info(dcfile.canonical_filepath)
            pdffile = [x for x in v if re_compile('.pdf$').search(x.canonical_filepath)][0]
            jpegfile = [x for x in v if 'JPEG' in x.canonical_filepath \
                        and '_0001' in x.canonical_filepath][0]
            ldrurl = LDRURL(join(directory, identifier))
            piurl = PIURL("dig/campub", join(directory, identifier))
            rightsurl = RightsURL()
            repurl = SubjectURL("http://repository.lib.uchicago.edu/")
            collectionurl = SubjectURL("ead/ICU.SPCL.CAMPUB")
            metsfile = [x for x in v 
                        if '.mets.xml' in x.canonical_filepath][0]
            metsresource = RDFSResource(join('/',metsfile.accession, 
                                             metsfile.dirhead,
                                             metsfile.canonical_filepath))
            metsresource.add_statement("dcterms:format", TextValue(metsfile.mimetype))
            webresource = WebResource(join('/', pdffile.accession, 
                                           pdffile.dirhead, 
                                           pdffile.canonical_filepath))
            webresource.add_statement("dcterms:isFormatOf", ldrurl)
            webresource.add_statement("premis:objectIdentifierType", 
                                      TextValue("ARK"))
            webresource.add_statement("premis:objectIdentifierValue", 
                                      webresource.subject)
            webresource.add_statement("dc:format", TextValue(pdffile.mimetype))
            webresource.add_statement("premis:objectCategory", 
                                      TextValue("file"))
            webresource.add_statement("premis:compositionLevel", IntegerValue(0))
            webresource.add_statement("premis:messageDigestAlgorithm", 
                                      TextValue("SHA-256")) 
            webresource.add_statement("premis:messageDigest", 
                                      TextValue(pdffile.checksum))
            webresource.add_statement("premis:messageDigestOriginator", 
                                      TextValue("/sbin/sha256"))
            webresource.add_statement("premis:size", IntegerValue(pdffile.file_size))
            webresource.add_statement("premis:formatName", 
                                      TextValue(pdffile.mimetype))
            webresource.add_statement("premis:originalName", 
                                      TextValue(pdffile.canonical_filepath))
            webresource.add_statement("premis:eventIdentifierType", 
                                      TextValue("ARK"))
            webresource.add_statement("premis:eventIdentifierValue", 
                                      TextValue(pdffile.accession))
            webresource.add_statement("premis:eventType", 
                                      TextValue("creation"))
            webresource.add_statement("premis:eventDateTime", 
                                      DateValue(createdate))
            pages = set([int(re_compile('_(\w{4}).*'). \
                             search(basename(x.canonical_filepath)). \
                             group(1).lstrip('0'))
                         for x in v if re_compile('_\w{4}.*'). \
                         search(basename(x.canonical_filepath))])

            numpages = list(pages)[-1]            
            providedcho = ProvidedCHO(join('/',directory))
            proxy = Proxy(join('/',dcfile.accession,dcfile.dirhead, 
                               dcfile.canonical_filepath))
            rem = ResourceMap(join('/rem',directory))
            aggregation = Aggregation(join('/aggregation',directory))
            aggregation.add_statement("edm:aggregationregatedCHO", 
                                      providedcho.subject)
            aggregation.add_statement("edm:dataProvider", 
                                      TextValue("University of Chicago Library"))
            aggregation.add_statement("edm:isShownAt", piurl)
            aggregation.add_statement("edm:isShownBy", 
                                      SubjectURL(join(pdffile.accession,
                                           pdffile.dirhead,
                                           pdffile.canonical_filepath)))
            aggregation.add_statement("edm:object", 
                                      SubjectURL(join(jpegfile.accession, 
                                               jpegfile.dirhead,
                                               jpegfile.canonical_filepath)))
            aggregation.add_statement("edm:provider", 
                                TextValue("University of Chicago Library"))
            aggregation.add_statement("dc:rights", rightsurl)
            aggregation.add_statement("ore:isDescribedBy", 
                                      rem.subject)
            aggregation.add_statement("dcterms:created", DateValue(createdate))
            aggregation.add_statement("dcterms:modified", DateValue(createdate))
            rem.add_statement("dcterms:created", DateValue(createdate))
            rem.add_statement("dcterms:modified", DateValue(createdate))
            rem.add_statement("dcterms:creator", repurl)
            rem.add_statement("ore:describes", aggregation.subject)


            providedcho.add_statement("dc:coverage",TextValue("Chicago"))
            providedcho.add_statement("dc:date", DateValue(dcfile.date))
            providedcho.add_statement("edm:year", 
                                      DateValue(dcfile.date.split('-')[0]))
            providedcho.add_statement("dc:description", 
                                      TextValue(dcfile.description))
            providedcho.add_statement("dc:identifier", 
                                      TextValue(identifier))
            providedcho.add_statement("dc:language", TextValue("en"))
            providedcho.add_statement("dc:rights", rightsurl)
            providedcho.add_statement("dc:title", TextValue(dcfile.title))
            providedcho.add_statement("dc:type", TextValue("text"))
            providedcho.add_statement("edm:type", TextValue("TEXT"))
            providedcho.add_statement("dc:description", 
                                      aggregation.subject)
            providedcho.add_statement("dcterms:isPartOf", collectionurl)
            providedcho.add_statement("dc:format", 
                                      TextValue(metsfile.mimetype))

            proxy.add_statement("dc:format", TextValue(dcfile.mimetype))
            proxy.add_statement("ore:proxyFor", providedcho.subject)
            proxy.add_statement("ore:proxyIn", aggregation.subject)
            stdout.write(str(proxy))
            stdout.write(str(rem))
            stdout.write(str(aggregation))
            stdout.write(str(webresource))
            stdout.write(str(metsresource))
            range_pages = [('0'*(4 - len(str(x)))) + str(x) for x in range(1,numpages+1)]
            for pos,i in enumerate(range_pages):
                logger.info("starting page {page} of {id}".format(page = i, 
                                                                  id = identifier))
                file_base = join('/',directory,identifier+'_'+i)
                agg_url = join('/aggregation',file_base)
                rem_url = join('/rem',file_base)
                tiff_file = join('/',directory,'TIFF',identifier+'_'+i)
                jpeg_file = join('/',directory,'JPEG',identifier+'_'+i)
                alto_file = join('/',directory,'ALTO',identifier+'_'+i)
                try:
                    tiffile = [x for x in v if 'TIFF' in x.canonical_filepath \
                               and str('_' + i) in \
                               x.canonical_filepath][0]
                    page_webresource = WebResource(join('/', tiffile.accession, 
                                                        tiffile.dirhead, 
                                                        tiffile.canonical_filepath))
                    page_webresource.add_statement("mix:fileSize", 
                                                   IntegerValue(tiffile.file_size))
                    page_webresource.add_statement("mix:formatName", 
                                                   TextValue(tiffile.mimetype))
                    page_webresource.add_statement("premis:objectIdentifierType", 
                                                   TextValue("ARK"))
                    page_webresource.add_statement("premis:objectIdentifierValue", 
                                                   page_webresource.subject)
                    page_webresource.add_statement("dc:format", TextValue(tiffile.mimetype))
                    page_webresource.add_statement("premis:objectCategory", 
                                                   TextValue("file"))
                    page_webresource.add_statement("premis:compositionLevel", IntegerValue(0))
                    page_webresource.add_statement("premis:messageDigestAlgorithm", 
                                                   TextValue("SHA-256")) 
                    page_webresource.add_statement("premis:messageDigest", 
                                                   TextValue(tiffile.checksum))
                    page_webresource.add_statement("premis:messageDigestOriginator", 
                                                   TextValue("/sbin/sha256"))
                    page_webresource.add_statement("premis:size", IntegerValue(tiffile.file_size))
                    page_webresource.add_statement("premis:formatName", 
                                                   TextValue(tiffile.mimetype))
                    page_webresource.add_statement("premis:originalName", 
                                                   TextValue(tiffile.canonical_filepath))
                    page_webresource.add_statement("premis:eventIdentifierType", 
                                                   TextValue("ARK"))
                    page_webresource.add_statement("premis:eventIdentifierValue", 
                                                   TextValue(tiffile.accession))
                    page_webresource.add_statement("premis:eventType", 
                                                   TextValue("creation"))
                    page_webresource.add_statement("premis:eventDateTime", 
                                                   DateValue(createdate))
                    if getattr(tiffile,'mixchecksum',None):
                        page_webresource.add_statement("mix:messageDigestAlgorithm", 
                                                       TextValue("MD5"))
                        page_webresource.add_statement("mix:messageDigest", 
                                                       TextValue(tiffile.mixchecksum))
                    if getattr(tiffile,'imageheight',None):
                        page_webresource.add_statement("mix:imageHeight",
                                                       IntegerValue(int(tiffile.imageheight)))
                    if getattr(tiffile,'imagewidth',None):
                        page_webresource.add_statement("mix:imageWidth", 
                                                       IntegerValue(int(tiffile.imagewidth)))
                    if getattr(tiffile,'bitspersample',None):
                        page_webresource.add_statement("mix:bitsPerSample",
                                                       TextValue(tiffile.bitspersample))
                    stdout.write(str(page_webresource))
                except IndexError:
                    logger.error("{page} from {record} is missing tiff".format(page = i, 
                                                                            record = identifier))                    
                try:
                    ocrfile = [x for x in v if 'ALTO' in x.canonical_filepath \
                               and str('_' + i) in \
                               x.canonical_filepath][0]
                    page_ocrresource = RDFSResource(join('/', ocrfile.accession,
                                                         ocrfile.dirhead,
                                                         ocrfile.canonical_filepath))
                    stdout.write(str(page_ocrresource))
                except IndexError:
                    logger.error("{page} from {record} is missing alto".format(page = i, 
                                                                            record = identifier))
                try:
                    jpegfile =  [x for x in v if 'JPEG' in \
                                 x.canonical_filepath \
                                 and str('_' + i) in \
                                 x.canonical_filepath][0]
                    page_jpegresource = RDFSResource(join('/', jpegfile.accession,
                                                          jpegfile.dirhead,
                                                          jpegfile.canonical_filepath))
                    page_jpegresource.add_statement("dc:format", 
                                                    TextValue(jpegfile.mimetype))
                    page_ocrresource.add_statement("dc:format",
                                                   TextValue(ocrfile.mimetype))
                    stdout.write(str(page_ocrresource))
                except IndexError:
                    logger.error("{page} from {record} is missing jpeg".format(page = i, 
                                                                            record = identifier))
                page_providedcho = ProvidedCHO(file_base)
                page_aggregation = Aggregation(agg_url)
                page_rem = ResourceMap(rem_url)
                page_aggregation.add_statement("edm:aggregatedCHO", 
                                               page_providedcho.subject)
                page_aggregation.add_statement("edm:dataProvider",
                                    TextValue("University of Chicago Library"))
                page_aggregation.add_statement("edm:isShownBy", 
                                               page_webresource.subject)
                page_aggregation.add_statement("edm:object", 
                                               page_jpegresource.subject)
                page_aggregation.add_statement("edm:provider", 
                                TextValue("University of Chicago Library"))
                page_aggregation.add_statement("edm:rights", 
                                               rightsurl)
                page_aggregation.add_statement("ore:isDescribedBy", 
                                               page_rem.subject)
                page_aggregation.add_statement("dcterms:created", DateValue(createdate))
                page_aggregation.add_statement("dcterms:modified", DateValue(createdate))
                page_rem.add_statement("dc:created", 
                                       DateValue(createdate))
                page_aggregation.add_statement("dcterms:modified", DateValue(createdate))
                page_rem.add_statement("dcterms:creator", 
                                       repurl)
                providedcho.add_statement("dcterms:hasPart",
                            SubjectURL(join(file_base)))
                page_providedcho.add_statement("dc:language", TextValue("en"))
                page_providedcho.add_statement("dc:rights", 
                                               rightsurl)
                page_providedcho.add_statement("dc:type", TextValue("Text"))
                page_providedcho.add_statement("edm:type", TextValue("TEXT"))
                page_providedcho.add_statement("dc:title", 
                                               TextValue("Page {number}". \
                                        format(number = i.lstrip('0'))))
                page_providedcho.add_statement("dcterms:isPartOf",
                                               providedcho.subject)
                if int(i.lstrip('0')) == numpages:
                    logger.info("last page")
                else:
                    next_page = range_pages[pos+1]
                    page_providedcho.add_statement("edm:isNextInSequence",
                        SubjectURL(join("/",directory, identifier+'_'+next_page)))

                stdout.write(str(page_providedcho))
                stdout.write(str(page_aggregation))
                stdout.write(str(page_rem))

                logger.info("finished page {page} of {id}".format(page = i, 
                                                            id = identifier))
            stdout.write(str(providedcho))
            logger.info("finished {id}".format(id = k))
        return 0
    except KeyboardInterrupt:
         logger.error("Program aborted manually")
         return 131

if __name__ == "__main__":
    _exit(main())
