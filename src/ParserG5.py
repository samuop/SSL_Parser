#LIBRERIAS
import ply.lex as lex
import ply.yacc as yacc
import os
import re
import codecs
from sys import stdin

bandera = False
flag = False
flag2 = False
#LEXER
tokens = [
    'DOCTYPE_ARTICLE',
    'XML_DECLARATION',
    'APERTURA_ARTICLE',
    'CIERRE_ARTICLE',
    'APERTURA_TITLE',
    'CIERRE_TITLE',
    'APERTURA_LINK',
    'regularEmail',
    'FILE_REF',
    'URL',
    'CIERRE_TAG',
    'APERTURA_SECTION',
    'CIERRE_SECTION',
    'APERTURA_SIMPLESECT',
    'CIERRE_SIMPLESECT',
    'APERTURA_COPY',
    'CIERRE_COPY',
    'APERTURA_IMAGDATA',
    'APERTURA_ITEMIZED',
    'CIERRE_ITEMIZED',
    'APERTURA_LISTITEM',
    'CIERRE_LISTITEM',
    'APERTURA_IMPORTANT',
    'CIERRE_IMPORTANT',
    'APERTURA_EMPHASIS',
    'CIERRE_EMPHASIS',
    'APERTURA_EMAIL',
    'CIERRE_EMAIL',
    'APERTURA_AUTOR',
    'CIERRE_AUTOR',
    'APERTURA_PN',
    'CIERRE_PN',
    'APERTURA_FNAME',
    'CIERRE_FNAME',
    'APERTURA_COMMENT',
    'CIERRE_COMMENT',
    'APERTURA_HOLDER',
    'CIERRE_HOLDER',
    'APERTURA_YEAR',
    'CIERRE_YEAR',
    'APERTURA_DATE',
    'CIERRE_DATE',
    'APERTURA_STREET',
    'CIERRE_STREET',
    'APERTURA_CITY',
    'CIERRE_CITY',
    'APERTURA_STATE',
    'CIERRE_STATE',
    'APERTURA_PHONE',
    'CIERRE_PHONE',
    'APERTURA_ADDRESS',
    'CIERRE_ADDRESS',
    'APERTURA_ABSTRACT',
    'CIERRE_ABSTRACT',
    'APERTURA_SIMPARA',
    'CIERRE_SIMPARA',
    'APERTURA_VIDEOOBJECT',
    'CIERRE_VIDEOOBJECT',
    'APERTURA_SURNAME',
    'CIERRE_SURNAME',
    'APERTURA_MEDIAOBJECT',
    'CIERRE_MEDIAOBJECT',
    'APERTURA_ENTRYTBL',
    'CIERRE_ENTRYTBL',
    'APERTURA_imageObjeto',
    'CIERRE_imageObjeto',
    'APERTURA_PARA',
    'CIERRE_PARA',
    'APERTURA_TBODY',
    'CIERRE_TBODY',
    'APERTURA_TFOOT',
    'CIERRE_TFOOT',
    'APERTURA_THEAD',
    'CIERRE_THEAD',
    'APERTURA_ENTRY',
    'CIERRE_ENTRY',
    'APERTURA_ROW',
    'CIERRE_ROW',
    'APERTURA_VIDEODATA',
    'C_VIDEODATAHTML',
    'CIERRE_TGrupo',
    'APERTURA_TGrupo',
    'CIERRE_InformalTable',
    'APERTURA_InformalTable',
    'CIERRE_INFO',
    'APERTURA_INFO',
    'TXT',
]


def t_DOCTYPE_ARTICLE(p):
    r'<!DOCTYPE\s+article>'
    return p


t_XML_DECLARATION = r'<\?xml\s+version="1\.0"\s+encoding="UTF-8"\?>'


def t_APERTURA_ARTICLE(p):
    r'\<article>'
    doc_html.write("<body>")
    return p


def t_CIERRE_ARTICLE(p):
    r'\</article>'
    text = "</body> \n </html>"
    doc_html.write(text)
    return p


def t_APERTURA_INFO(p):
    r'<info>'
    doc_html.write(
        '<p style=\"background-color: green; color: white; font-size:8px;\"> INFO: '
    )
    return p


def t_CIERRE_INFO(p):
    r'</info>'
    doc_html.write('</p>')
    return p


def t_APERTURA_TITLE(p):
    r'<title>'
    global bandera
    if bandera == False:
        doc_html.write("<h1>")
    else:
        doc_html.write("<h2>")
    return p


def t_CIERRE_TITLE(p):
    r'</title>'
    global bandera
    if bandera == False:
        doc_html.write("</h1>")
    else:
        doc_html.write("</h2>")
    return p


def t_APERTURA_LINK(p):
    r'<link\s+xlink:href=\"'
    global flag2
    flag2 = True
    doc_html.write("<a href=\"")
    return p

def t_FILE_REF(p):
    r'([a-zA-Z0-9\/_.-]+\.(png|jpg|jpeg|gif|mp4))'
    doc_html.write(p.value)
    return p

def t_URL(p):
    r'(http|https|ftp|ftps):\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
    global flag2
    if flag2 == True:
        doc_html.write(str(p.value)+"\""+">"+ str(p.value))
    else:
        doc_html.write(p.value)
    return p


t_ignore = r'\t'

def t_regularEmail(p):
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]'
    doc_html.write(p.value)
    return (p)

def t_APERTURA_SECTION(p):
    r'\<section>'
    global bandera
    bandera = True
    etiqueta_html = '<p style="background-color: green; color: white; font-size: 8pt;">'
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_SECTION(p):
    r'\</section>'
    global bandera
    bandera = False
    etiqueta_html = '</p>'
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_SIMPLESECT(p):
    r'\<simplesect>'
    global bandera
    bandera = True
    doc_html.write("<div>")
    return p


def t_CIERRE_SIMPLESECT(p):
    r'\</simplesect>'
    global bandera
    bandera = False
    doc_html.write("</div>")
    return p


def t_APERTURA_COPY(p):
    r'\<copyright>'
    doc_html.write("&copy;")
    return p


def t_CIERRE_COPY(p):
    r'\</copyright>'
    return p


def t_APERTURA_IMAGDATA(p):
    r'<imagedata\s+fileref=\"'
    doc_html.write('<img width="500" height="400" src="')
    return p


def t_APERTURA_ITEMIZED(p):
    r'\<itemizedlist>'
    doc_html.write("<ul>")
    return p


def t_CIERRE_ITEMIZED(p):
    r'\</itemizedlist>'
    doc_html.write("</ul>")
    return p


def t_APERTURA_LISTITEM(p):
    r'\<listitem>'
    doc_html.write("<li>")
    return p


def t_CIERRE_LISTITEM(p):
    r'\</listitem>'
    doc_html.write("</li>")
    return p


def t_APERTURA_IMPORTANT(p):
    r'<important>'
    etiqueta_html = "<p style=\"background-color: red; color: white; font-size:24px;\"> IMPORTANTE: "
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_IMPORTANT(p):
    r'</important>'
    etiqueta_html = "</p>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_EMPHASIS(p):
    r'<emphasis>'
    etiqueta_html = "<em>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_EMPHASIS(p):
    r'</emphasis>'
    etiqueta_html = "</em>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_EMAIL(p):
    r'<email>'
    etiqueta_html = "<a href=\"mailto:\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_EMAIL(p):
    r'</email>'
    etiqueta_html = "</a>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_AUTOR(p):
    r'<author>'
    etiqueta_html = "<div class=\"author\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_AUTOR(p):
    r'</author>'
    etiqueta_html = "</div>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_PN(p):
    r'\<personname>'
    etiqueta_html = '<span style="background-color: green; color: white; font-size: 8pt;">'
    doc_html.write(etiqueta_html)
    return p

def t_CIERRE_PN(p):
    r'\</personname>'
    etiqueta_html = '</span>'
    doc_html.write(etiqueta_html)
    return p

def t_APERTURA_FNAME(p):
    r'<firstname>'
    etiqueta_html = "<span class=\"firstname\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_FNAME(p):
    r'</firstname>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_COMMENT(p):
    r'<comment>'
    etiqueta_html = "<!-- "
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_COMMENT(p):
    r'</comment>'
    etiqueta_html = " -->"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_HOLDER(p):
    r'<holder>'
    etiqueta_html = "<div class=\"holder\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_HOLDER(p):
    r'</holder>'
    etiqueta_html = "</div>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_YEAR(p):
    r'<year>'
    etiqueta_html = "<span class=\"year\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_YEAR(p):
    r'</year>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_DATE(p):
    r'<date>'
    etiqueta_html = "<span class=\"date\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_DATE(p):
    r'</date>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_STREET(p):
    r'\<street>'
    etiqueta_html = "<span class=\"street\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_STREET(p):
    r'\</street>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_CITY(p):
    r'\<city>'
    etiqueta_html = "<span class=\"city\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_CITY(p):
    r'\</city>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_PHONE(p):
    r'\<phone>'
    etiqueta_html = "<span class=\"phone\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_PHONE(p):
    r'\</phone>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_STATE(p):
    r'\<state>'
    etiqueta_html = "<span class=\"state\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_STATE(p):
    r'\</state>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_ADDRESS(p):
    r'\<address>'
    etiqueta_html = "<address>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_ADDRESS(p):
    r'\</address>'
    etiqueta_html = "</address>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_ABSTRACT(p):
    r'\<abstract>'
    etiqueta_html = "<div class=\"abstract\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_ABSTRACT(p):
    r'\</abstract>'
    etiqueta_html = "</div>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_SIMPARA(p):
    r'\<simpara>'
    etiqueta_html = "<p>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_SIMPARA(p):
    r'\</simpara>'
    etiqueta_html = "</p>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_VIDEOOBJECT(p):
    r'\<videoobject>'
    etiqueta_html = "<div class=\"videoobject\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_VIDEOOBJECT(p):
    r'\</videoobject>'
    etiqueta_html = "</div>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_SURNAME(p):
    r'\<surname>'
    etiqueta_html = "<span class=\"surname\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_SURNAME(p):
    r'\</surname>'
    etiqueta_html = "</span>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_MEDIAOBJECT(p):
    r'\<mediaobject>'
    etiqueta_html = "<div class=\"mediaobject\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_MEDIAOBJECT(p):
    r'\</mediaobject>'
    etiqueta_html = "</div>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_ENTRY(p):
    r'\<entry>'
    etiqueta_html = "<div class=\"entry\">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_ENTRY(p):
    r'\</entry>'
    etiqueta_html = "</div>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_ENTRYTBL(p):
    r'\<entrytbl\s*(align="[^"]*"|char="[^"]*"|charoff="\d+"|colname="[^"]*"|cols="\d+"|colsep="\d+"|nameed="[^"]*"|namest="[^"]*"|rowsep=\d+|spanname="\d+"|tgroupstyle="\d+")*\s*>'
    etiqueta_html = "<table"

    atributos = p[0].split()[1:]

    for atributo in atributos:
        etiqueta_html += " " + atributo

    etiqueta_html += ">"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_ENTRYTBL(p):
    r'\</entrytbl>'
    etiqueta_html = "</table>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_imageObjeto(p):
    r'\<imageobject>'
    doc_html.write('<div class="imageobject">')
    return p


def t_CIERRE_imageObjeto(p):
    r'\</imageobject>'
    doc_html.write('<div>')
    return p


def t_APERTURA_PARA(p):
    r'\<para>'
    etiqueta_html = "<p>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_PARA(p):
    r'\</para>'
    etiqueta_html = "</p>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_ROW(p):
    r'\<row>'
    etiqueta_html = "<tr>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_ROW(p):
    r'\</row>'
    etiqueta_html = "</tr>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_TBODY(p):
    r'\<tbody>'
    etiqueta_html = "<tbody>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_TBODY(p):
    r'\</tbody>'
    etiqueta_html = "</tbody>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_TFOOT(p):
    r'\<tfoot>'
    etiqueta_html = "<tfoot>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_TFOOT(p):
    r'\</tfoot>'
    etiqueta_html = "</tfoot>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_THEAD(p):
    r'\<thead>'
    etiqueta_html = "<thead>"
    doc_html.write(etiqueta_html)
    return p


def t_CIERRE_THEAD(p):
    r'\</thead>'
    etiqueta_html = "</thead>"
    doc_html.write(etiqueta_html)
    return p


def t_APERTURA_InformalTable(p):
    r'<informaltable\s*(colsep="\d+"|frame="(above|all|below|border|bottom|box|hsides|lhs|none|rhs|sides|top|topbot|void)"|label|orient="(land|port)"|pgwide="\d+"|rowsep="\d+"|rowheader="(firstcol|headers|norowheader)"|tabstyle|tocentry)*\s*>'
    doc_html.write("<table>")
    return p


def t_CIERRE_InformalTable(p):
    r'\</informaltable>'
    doc_html.write("</table>")
    return p


def t_APERTURA_TGrupo(p):
    r'<tgroup\s*(align="[^"]*"|char="[^"]*"|charoff="\d+"|colname="[^"]*"|cols="\d+"|colsep="\d+"|nameed="[^"]*"|namest="[^"]*"|rowsep=\d+|spanname="\d+"|tgroupstyle="\d+")*\s*>'
    doc_html.write("<colgroup>")
    return p


def t_CIERRE_TGrupo(p):
    r'\</tgroup>'
    doc_html.write("</colgroup>")
    return p


def t_APERTURA_VIDEODATA(p):
    r'\<videodata\s+fileref=\"'
    doc_html.write('<iframe width="560" height="315" src="')
    global flag
    flag = True
    return p


def t_CIERRE_TAG(p):
    r'\"\s*\/>'
    global flag, flag2
    if flag == True:
        doc_html.write('"frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>')
        flag = False
    elif flag2 == True:
        doc_html.write('</a>')
        flag2 = False
    else:
        doc_html.write('">')
    return p


def t_TXT(p):
    r'[a-zA-Z0-9][a-zA-Z.,:\:\+\t\-\_ áéíóú0-9\@]*'
    doc_html.write(p.value)
    return p


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    doc_html.write("\n")


def t_COMMENT(t):
    r'\#.*'
    pass


def t_error(t):

    t.lexer.skip(1)


#
def p_sigma(p):
    '''sigma : DOCTYPE_ARTICLE articulo
             | XML_DECLARATION articulo
             | DOCTYPE_ARTICLE XML_DECLARATION articulo
    '''
    print("Archivo correctamente codificado, sin errores")


def p_articulo(p):
    '''articulo : APERTURA_ARTICLE raiz CIERRE_ARTICLE'''
    print("article: ", p[1], p[len(p) - 1])


def p_raiz(p):
    '''
    raiz : informacion titulo options opsections
         | informacion options opsections
         | titulo options opsections
         | options opsections
         | options
         | informacion titulo options
         | informacion options
         | titulo options
    '''


def p_options(p):
    '''
    options : ItemLista
            | Importante
            | PARA
            | simplePara
            | Direccion
            | MediaObjeto
            | InformalTable
            | Comment
            | titulo
            | Abstracto
            | seccion
            | ItemLista options
            | Importante options
            | PARA options
            | simplePara options
            | Direccion options
            | MediaObjeto options
            | InformalTable options
            | Comment options
            | Abstracto options
            | seccion options
    '''


def p_opsections(p):
    '''
    opsections : seccionSimple
               | seccion
               | seccionSimple opsections
               | seccion opsections
    '''


def p_seccion(p):
    ''' seccion : APERTURA_SECTION raiz CIERRE_SECTION '''
    print("section: ", p[1], p[len(p) - 1])


def p_seccionSimple(p):
    ''' 
  seccionSimple : APERTURA_SIMPLESECT informacion titulo options CIERRE_SIMPLESECT
                | APERTURA_SIMPLESECT informacion options CIERRE_SIMPLESECT
                | APERTURA_SIMPLESECT titulo options CIERRE_SIMPLESECT
  '''
    print("simple section: ", p[1], p[len(p) - 1])


def p_ItemLista(p):
    '''
    ItemLista : APERTURA_ITEMIZED Listatemas CIERRE_ITEMIZED
              | APERTURA_ITEMIZED Listatemas CIERRE_ITEMIZED ItemLista
    '''
    print("itemizedList: ", p[1], p[len(p) - 1])


def p_Listatemas(p):
    '''
    Listatemas : APERTURA_LISTITEM options CIERRE_LISTITEM
               | APERTURA_LISTITEM options CIERRE_LISTITEM Listatemas
    '''
    print("listItem: ", p[1], p[3])


def p_Importante(p):
    '''
    Importante : APERTURA_IMPORTANT titulo options CIERRE_IMPORTANT
               | APERTURA_IMPORTANT options CIERRE_IMPORTANT
    '''
    print("important: ", p[1], p[len(p) - 1])


def p_titulo(p):
    '''
    titulo : APERTURA_TITLE OpTitulo CIERRE_TITLE
           | APERTURA_TITLE OpTitulo CIERRE_TITLE titulo
    '''
    print("title: ", p[1], p[len(p) - 1])


def p_OpTitulo(p):
    '''
    OpTitulo : TXT
             | Emphasis
             | Link
             | Email
             | TXT OpTitulo
             | Emphasis OpTitulo
             | Link OpTitulo
             | Email OpTitulo
    '''


def p_Emphasis(p):
    '''
    Emphasis : APERTURA_EMPHASIS OpEmphasis CIERRE_EMPHASIS
    '''
    print("Emphasis: ", p[1], p[len(p) - 1])


def p_OpEmphasis(p):
    '''
    OpEmphasis : TXT
               | Link
               | Email
               | Author
               | Emphasis
               | Comment
               | TXT OpEmphasis
               | Link OpEmphasis
               | Email OpEmphasis
               | Author OpEmphasis
               | Comment OpEmphasis
    '''


def p_Link(p):
    '''Link : APERTURA_LINK URL CIERRE_TAG'''
    print("Link: ", p[1], p[2], p[len(p) - 1])


def p_informacion(p):
    '''informacion : APERTURA_INFO infoOptions CIERRE_INFO'''
    print("Info: ", p[1], p[len(p) - 1])


def p_infoOptions(p):
    '''
    infoOptions : MediaObjeto
                | Abstracto
                | Direccion
                | Author
                | Fecha
                | COPY
                | titulo
                | MediaObjeto infoOptions
                | Abstracto infoOptions
                | Direccion infoOptions
                | Author infoOptions
                | Fecha infoOptions
                | COPY infoOptions
                | titulo infoOptions
    '''


def p_MediaObjeto(p):
    '''
    MediaObjeto : APERTURA_MEDIAOBJECT informacion opMedia CIERRE_MEDIAOBJECT
                | APERTURA_MEDIAOBJECT informacion opMedia CIERRE_MEDIAOBJECT MediaObjeto
                | APERTURA_MEDIAOBJECT opMedia CIERRE_MEDIAOBJECT
                | APERTURA_MEDIAOBJECT opMedia CIERRE_MEDIAOBJECT MediaObjeto
    '''
    print("MediaObject: ", p[1], p[len(p) - 1])


def p_opMedia(p):
    '''
    opMedia : VideoObjeto
            | ImageObjeto
            | VideoObjeto opMedia
            | ImageObjeto opMedia
    '''


def p_VideoObjeto(p):
    '''
    VideoObjeto : APERTURA_VIDEOOBJECT informacion VideoData CIERRE_VIDEOOBJECT
                | APERTURA_VIDEOOBJECT VideoData CIERRE_VIDEOOBJECT
    '''
    print("VideoObject: ", p[1], p[len(p) - 1])


def p_VideoData(p):
    '''VideoData : APERTURA_VIDEODATA URL CIERRE_TAG
                | APERTURA_VIDEODATA FILE_REF CIERRE_TAG
    '''
    print("VideoData: ", p[1], p[len(p) - 1])


def p_ImageObjeto(p):
    '''
    ImageObjeto : APERTURA_imageObjeto informacion imageData CIERRE_imageObjeto
                | APERTURA_imageObjeto imageData CIERRE_imageObjeto
    '''
    print("ImageObject: ", p[1], p[len(p) - 1])


def p_imageData(p):
    '''imageData : APERTURA_IMAGDATA FILE_REF CIERRE_TAG
                | APERTURA_IMAGDATA URL CIERRE_TAG
    '''
    print("ImageData: ", p[1], p[len(p) - 1])


def p_Abstracto(p):
    '''
    Abstracto : APERTURA_ABSTRACT opAbstracto CIERRE_ABSTRACT
            | APERTURA_ABSTRACT titulo opAbstracto CIERRE_ABSTRACT
    '''
    print("Abstract: ", p[1], p[len(p) - 1])


def p_opAbstracto(p):
    '''
    opAbstracto : PARA
                | PARA opAbstracto
                | simplePara opAbstracto
                | simplePara
    '''


def p_simplePara(p):
    '''
    simplePara : APERTURA_SIMPARA OpSECL CIERRE_SIMPARA
    '''
    print("SimPara: ", p[1], p[len(p) - 1])


def p_PARA(p):
    '''
    PARA : APERTURA_PARA opPARA CIERRE_PARA
    '''
    print("Para: ", p[1], p[len(p) - 1])


def p_opPARA(p):
    '''
    opPARA : TXT
           | Emphasis
           | Link
           | Email
           | Author
           | Comment
           | ItemLista
           | Importante
           | Direccion
           | MediaObjeto
           | InformalTable
           | TXT opPARA
           | Emphasis opPARA
           | Link opPARA
           | Email opPARA
           | Author opPARA
           | Comment opPARA
           | ItemLista opPARA
           | Importante opPARA
           | Direccion opPARA
           | MediaObjeto opPARA
           | InformalTable opPARA
    '''


def p_InformalTable(p):
    '''
    InformalTable : APERTURA_InformalTable MediaObjeto CIERRE_InformalTable
                | APERTURA_InformalTable TGrupo CIERRE_InformalTable
                | APERTURA_InformalTable titulo MediaObjeto CIERRE_InformalTable
    '''
    print("InformalTable : ",p[1], p[len(p)-1])



def p_TGrupo(p):
    '''
    TGrupo : APERTURA_TGrupo opTG CIERRE_TGrupo
            | APERTURA_TGrupo opTG CIERRE_TGrupo TGrupo
    '''
    print("TGroup: ", p[1], p[len(p) - 1])


def p_opTG(p):
    '''
    opTG : THEAD TFOOT TBODY
         | TBODY
         | THEAD TBODY
         | TFOOT TBODY
    '''


def p_THEAD(p):
    '''
    THEAD : APERTURA_THEAD ROW CIERRE_THEAD
    '''
    print("THead: ", p[1], p[len(p) - 1])


def p_TFOOT(p):
    '''
    TFOOT : APERTURA_TFOOT ROW CIERRE_TFOOT
    '''
    print("TFoot", p[1], p[len(p) - 1])


def p_TBODY(p):
    '''
    TBODY : APERTURA_TBODY ROW CIERRE_TBODY
    '''
    print("TBody", p[1], p[len(p) - 1])


def p_ROW(p):
    '''
    ROW : APERTURA_ROW opROW CIERRE_ROW
        | APERTURA_ROW opROW CIERRE_ROW ROW
    '''
    print("Row: ", p[1], p[len(p) - 1])


def p_opROW(p):
    '''
    opROW : ENTRY
          | ENTRYBL
          | ENTRY opROW
          | ENTRYBL opROW
    '''


def p_ENTRY(p):
    '''
    ENTRY : APERTURA_ENTRY opEN CIERRE_ENTRY
    '''
    print("Entry: ", p[1], p[len(p) - 1])


def p_opEN(p):
    '''
    opEN : TXT
         | ItemLista
         | Importante
         | PARA
         | simplePara
         | MediaObjeto
         | Comment
         | Abstracto
         | TXT opEN
         | ItemLista opEN
         | Importante opEN
         | PARA opEN
         | simplePara opEN
         | MediaObjeto opEN
         | Comment opEN
         | Abstracto opEN
    '''


def p_ENTRYBL(p):
    '''
    ENTRYBL : APERTURA_ENTRYTBL THEAD TBODY CIERRE_ENTRYTBL
            | APERTURA_ENTRYTBL TBODY CIERRE_ENTRYTBL
    '''
    print("Entrybl: ", p[1], p[len(p) - 1])


def p_Direccion(p):
    '''
    Direccion : APERTURA_ADDRESS CIERRE_ADDRESS
                | APERTURA_ADDRESS opAddress CIERRE_ADDRESS
    '''
    print("Direccion: ", p[1], p[len(p) - 1])


def p_opAddress(p):
    '''
    opAddress : TXT
              | calle
              | ciudad
              | estado
              | telefono
              | Email
              | TXT opAddress
              | calle opAddress
              | ciudad opAddress
              | estado opAddress
              | telefono opAddress
              | Email opAddress
    '''


def p_calle(p):
    '''
    calle : APERTURA_STREET opDatos CIERRE_STREET
    '''
    print("Calle: ", p[1], p[len(p) - 1])


def p_ciudad(p):
    '''
    ciudad : APERTURA_CITY opDatos CIERRE_CITY
    '''
    print("Ciudad: ", p[1], p[len(p) - 1])


def p_estado(p):
    '''
    estado : APERTURA_STATE opDatos CIERRE_STATE
    '''
    print("Estado: ", p[1], p[len(p) - 1])


def p_Email(p):
    '''
    Email : APERTURA_EMAIL opEmail CIERRE_EMAIL
    '''
    print("Email: ", p[1], p[len(p) - 1])


def p_opEmail(p):
    '''
    opEmail : regularEmail
            | Link
            | Emphasis
            | Comment
            | regularEmail opEmail
            | Link opEmail
            | Emphasis opEmail
            | Comment opEmail
    '''


def p_telefono(p):
    '''
    telefono : APERTURA_PHONE opDatos CIERRE_PHONE
    '''
    print("Telefono: ", p[1], p[len(p) - 1])


def p_Author(p):
    '''
    Author : APERTURA_AUTOR personName CIERRE_AUTOR
            | APERTURA_AUTOR opPersonname CIERRE_AUTOR
    '''
    print("Author: ", p[1], p[len(p) - 1])


def p_personName(p):
    '''
    personName : APERTURA_PN opPersonname CIERRE_PN
    '''


def p_opPersonname(p):
    '''
    opPersonname : Firstname
             | Surname
             | Firstname opPersonname
             | Surname opPersonname
    '''


def p_Firstname(p):
    '''
    Firstname : APERTURA_FNAME opDatos CIERRE_FNAME
    '''
    print("Firstname: ", p[1], p[len(p) - 1])


def p_Surname(p):
    '''
    Surname : APERTURA_SURNAME opDatos CIERRE_SURNAME
    '''
    print("Surname: ", p[1], p[len(p) - 1])


def p_Fecha(p):
    '''
    Fecha : APERTURA_DATE TXT CIERRE_DATE
    '''
    print("Fecha: ", p[1], p[len(p) - 1])


def p_COPY(p):
    '''
    COPY : APERTURA_COPY YEAR CIERRE_COPY
         | APERTURA_COPY YEAR titular opAbstracto CIERRE_COPY
    '''
    print("Copyrigth: ", p[1], p[len(p) - 1])


def p_YEAR(p):
    '''YEAR : APERTURA_YEAR opDatos CIERRE_YEAR
          | APERTURA_YEAR opDatos CIERRE_YEAR YEAR
  '''
    print("Year: ", p[1], p[len(p) - 1])


def p_titular(p):
    '''
    titular : APERTURA_HOLDER opDatos CIERRE_HOLDER
            | APERTURA_HOLDER opDatos CIERRE_HOLDER titular
    '''
    print("Titular: ", p[1], p[len(p) - 1])


def p_opDatos(p):
    '''
    opDatos : TXT
            | Link
            | Emphasis
            | Comment
            | TXT opDatos
            | Link opDatos
            | Emphasis opDatos
            | Comment opDatos
    '''


def p_Comment(p):
    '''
    Comment : APERTURA_COMMENT OpSECL CIERRE_COMMENT
    '''
    print("Comment: ", p[1], p[len(p) - 1])


def p_OpSECL(p):
    '''
    OpSECL : TXT
           | Emphasis
           | Link
           | Email
           | Author
           | Comment
           | TXT OpSECL
           | Emphasis OpSECL
           | Link OpSECL
           | Email OpSECL
           | Author OpSECL
           | Comment OpSECL
    '''


def p_error(p):
    if p is not None:
        print("Error de sintaxis:", p)
        print("El error se produjo en la línea", str(p.lineno))
    else:
        print("Error de sintaxis: Se alcanzó el final inesperado del archivo")


#OTRAS FUNCIONES
def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print(str(cont) + ". " + file)
        cont = cont + 1

    while respuesta == False:
        numArchivo = input('\nNumero del test: ')
        for file in files:
            if file == files[int(numArchivo) - 1]:
                respuesta = True
                break

    print("Tags reconocidos en el archivo \"%s\" \n" %
          files[int(numArchivo) - 1])

    return files[int(numArchivo) - 1]


#PROCESO
directorio = "test/"
archivo = buscarFicheros(directorio)
test = directorio + archivo
fp = codecs.open(test, "r", "UTF-8")
cadena = fp.read()
fp.close()


def evaluar_extension(archivo):
    _, extension = os.path.splitext(archivo)
    return extension


extension = evaluar_extension(archivo)

if evaluar_extension(archivo) == ".txt":
    doc_html = open(archivo.replace(".txt", ".html"), "w")
else:
    doc_html = open(archivo.replace(".xml", ".html"), "w")

doc_html.write("<!DOCTYPE html>\n<html>")
analizador = lex.lex()
parser = yacc.yacc()
result = parser.parse(cadena)

print(result)
doc_html.close()
input()

