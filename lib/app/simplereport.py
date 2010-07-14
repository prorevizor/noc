# -*- coding: utf-8 -*-
##----------------------------------------------------------------------
## SimpleReport implementation
##----------------------------------------------------------------------
## Copyright (C) 2007-2009 The NOC Project
## See LICENSE for details
##----------------------------------------------------------------------
from reportapplication import *
import cStringIO,csv,datetime
from noc import settings
from django.utils.dateformat import DateFormat
import decimal,types

INDENT="    "
##
## Abstract Report Node
##
class ReportNode(object):
    tag=None
    def __init__(self,name=None):
        self.name=name
    ##
    ## Return XML-quoted value
    ##
    def quote(self,s):
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\"","&quot").replace("'","&#39;")
    ##
    ## Return opening XML tag
    ##
    def format_opening_xml_tag(self,**kwargs):
        s="<%s"%self.tag
        for k,v in kwargs.items():
            if v:
                s+=" %s='%s'"%(k,self.quote(v))
        s+=">"
        return s
    ##
    ## Return closing XML tag
    ##
    def format_closing_xml_tag(self):
        return "</%s>"%self.tag
    ##
    ## Indent block of code
    ##
    def indent(self,s,n=1):
        i=INDENT*n
        return i+s.replace("\n","\n"+i)
    ##
    ## Return XML presentation of Node
    ##
    def to_xml(self):
        return ""
    ##
    ## Return HTML presentation of Node
    ##
    def to_html(self):
        return ""
    ##
    ## Return CSV presentation of Node
    ##
    def to_csv(self):
        return ""
##
## Report root node
##
class Report(ReportNode):
    tag="report"
    def __init__(self,name=None):
        super(Report,self).__init__(name=name)
        self.sections=[] # Must be ReportSection instances
    
    def append_section(self,s):
        self.sections+=[s]
    ##
    ## Return XML code for report
    ##
    def to_xml(self):
        s=[self.format_opening_xml_tag(name=self.name)]
        s+=[self.indent("<sections>")]
        s+=[self.indent(x.to_xml(),2) for x in self.sections]
        s+=[self.indent("</sections>")]
        s+=[self.format_closing_xml_tag()]
        return "\n".join(s)
    ##
    ## Return HTML code for report
    ##
    def to_html(self):
        return "\n".join([s.to_html() for s in self.sections])
    ##
    ## Return CSV for report
    ##
    def to_csv(self):
        return "\n".join([x for x in [s.to_csv() for s in self.sections] if x])
##
## Abstract class for report sections
##
class ReportSection(ReportNode): pass
##
## Section containing text. Consists of title and text
## text bay be string or list of paragraphs.
## Skipped in CSV mode
##
class TextSection(ReportSection):
    tag="text"
    def __init__(self,name=None,title=None,text=None):
        super(ReportSection,self).__init__(name=name)
        self.title=title
        self.text=text # Either string o list of strings
    ##
    ## Returns a list of paragraphs
    ##
    def paragraphs(self):
        if not self.text:
            return []
        if isinstance(self.text,basestring):
            return [self.text]
        else:
            return self.text
    paragraphs=property(paragraphs)
    ##
    ## Return XML presentation of text section
    ##
    def to_xml(self):
        s=[self.format_opening_xml_tag(name=self.name,title=self.title)]
        s+=[self.indent("<par>%s</par>"%self.quote(p)) for p in self.paragraphs]
        s+=[self.format_closing_xml_tag()]
        return "\n".join(s)
    ##
    ## Return HTML presentation of text section
    ##
    def to_html(self):
        s=[]
        if self.title:
            s+=["<h2>%s</h2>"%self.quote(self.title)]
        s+=["<p>%s</p>"%self.quote(p) for p in self.paragraphs]
        return "\n".join(s)

##
## Precomputed size multipliers
## List of (limit,divider,suffix)
##
SIZE_DATA=[]
l=decimal.Decimal(1024)
for suffix in ["KB","MB","GB","TB","PB"]:
    SIZE_DATA+=[(l*1024,l,suffix)]
    l*=1024
##
## Do not perform HTML quoting
##
class SafeString(str): pass
##
## Table column.
## Contains rules for formatting the cells
##
class TableColumn(ReportNode):
    tag="column"
    ALIGN_LEFT=1
    ALIGN_RIGHT=2
    ALIGN_CENTER=3
    H_ALIGN_MASK=3
    def __init__(self,name,title=None,align=None,format=None,total=None,total_label=None):
        self.name=name
        self.title=title if title else name
        self.align={"l":self.ALIGN_LEFT,   "left":self.ALIGN_LEFT,
                    "r":self.ALIGN_RIGHT,  "right":self.ALIGN_RIGHT,
                    "c":self.ALIGN_CENTER, "center":self.ALIGN_CENTER}[align.lower()] if align else None
        self.format=getattr(self,"f_%s"%format) if isinstance(format,basestring) else format
        self.total=getattr(self,"ft_%s"%total) if isinstance(total,basestring) else total
        self.total_label=total_label
        self.total_data=[]
        self.subtotal_data=[]
    ##
    ## Check column has total
    ##
    def has_total(self):
        return self.total
    has_total=property(has_total)
    ##
    ## Reset sub-totals
    ##
    def start_section(self):
        self.subtotal_data=[]
    ##
    ## Contribute data to totals
    ##
    def contribute_data(self,s):
        if self.total:
            self.total_data+=[s]
    ##
    ## Return formatted cell
    ##
    def format_data(self,s):
        if s is None or s=="":
            return ""
        elif not self.format:
            return s
        else:
            return self.format(s)
    ##
    ## Return XML representation of column
    ##
    def to_xml(self):
        return self.format_opening_xml_tag(name=self.name,align=self.align)+self.quote(self.title)+self.format_closing_xml_tag()
    ##
    ## Return quoted HTML TD attributes
    ##
    def html_td_attrs(self):
        attrs={}
        if self.align:
            if self.align&self.H_ALIGN_MASK==self.ALIGN_LEFT:
                attrs["align"]="left"
            elif self.align&self.H_ALIGN_MASK==self.ALIGN_RIGHT:
                attrs["align"]="right"
            elif self.align&self.H_ALIGN_MASK==self.ALIGN_CENTER:
                attrs["align"]="center"
        return " "+" ".join(["%s='%s'"%(k,self.quote(v)) for k,v in attrs.items()])
    ##
    ## Render single cell
    ##
    def format_html(self,s):
        d=self.format_data(s)
        if type(d)!=SafeString:
            d=self.quote(d)
        return "<td%s>%s</td>"%(self.html_td_attrs(),d)
    ##
    ## Render totals
    ##
    def format_html_total(self):
        if self.total:
            total=self.format_data(self.total(self.total_data))
        elif self.total_label:
            total=self.total_label
        else:
            total=""
        return "<td%s><b>%s</b></td>"%(self.html_td_attrs(),total)
    ##
    ## Display date according to settings
    ##
    def f_date(self,f):
        return DateFormat(f).format(settings.DATE_FORMAT)
    ##
    ## Display time according to settings
    ##
    def f_time(self,f):
        return DateFormat(f).format(settings.TIME_FORMAT)
    ##
    ## Display date and time according to settings
    ##
    def f_datetime(self,f):
        return DateFormat(f).format(settings.DATETIME_FORMAT)
    ##
    ## Display pretty size
    ##
    def f_size(self,f):
        f=decimal.Decimal(f)
        for limit,divider,suffix in SIZE_DATA:
            if f<limit:
                return ("%8.2f%s"%(f/divider,suffix)).strip()
        limit,divider,suffix=SIZE_DATA[-1]
        return ("%8.2%s"%(f/divider,suffix)).strip()
    ##
    ## Display pretty numeric
    ##
    def f_numeric(self,f):
        if not f:
            return "0"
        if type(f)==types.FloatType:
            f=str(f)
        f=decimal.Decimal(f)
        sign,digits,exp=f.as_tuple()
        if exp:
            r="."+"".join(map(str,digits[-exp:]))
            if r==".0":
                r=""
            digits=digits[:exp]
        else:
            r=""
        while digits:
            r=" "+"".join(map(str,digits[-3:]))+r
            digits=digits[:-3]
        r=r.strip()
        if sign:
            r="-"+r
        return r
    ##
    ## Display boolean field
    ##
    def f_bool(self,f):
        t="yes" if f else "no"
        return SafeString("<img title='%s' src='%simg/admin/icon-%s.gif' />"%(t,settings.ADMIN_MEDIA_PREFIX,t))
    ##
    ## Display pretty-formatted integer
    ##
    def f_integer(self,f):
        return self.f_numeric(int(f))
    ##
    ## Returns a sum of not-null elements
    ##
    def ft_sum(self,l):
        return reduce(lambda x,y:x+y,[decimal.Decimal(str(z)) for z in l if z],0)
##
## Section containing table
##
##
class TableSection(ReportSection):
    tag="table"
    def __init__(self,name=None,columns=[],enumerate=False,data=[]):
        super(ReportSection,self).__init__(name=name)
        self.columns=[]
        for c in columns:
            if isinstance(c,basestring):
                self.columns+=[TableColumn(c)]
            else:
                self.columns+=[c]
        self.data=data
        self.enumerate=enumerate
        self.has_total=reduce(lambda x,y: x or y,[c.has_total for c in self.columns],False) # Check wrether table has totals
    ##
    ## Return XML representation of table
    ##
    def to_xml(self):
        s=[self.format_opening_xml_tag(name=self.name)]
        s+=[self.indent("<columns>")]
        s+=[self.indent(c.to_xml(),2) for c in self.columns]
        s+=[self.indent("</columns>")]
        s+=[self.format_closing_xml_tag()]
        return "\n".join(s)
    ##
    ## Return HTML representation of table
    ##
    def to_html(self):
        s=["<table class='report-table' summary='%s'>"%self.quote(self.name)]
        # Render header
        s+=["<thead>"]
        s+=["<tr>"]
        if self.enumerate:
            s+=["<th>#</th>"]
        s+=["<th>%s</th>"%self.quote(c.title) for c in self.columns]
        s+=["</tr>"]
        s+=["</thead>"]
        s+=["<tbody>"]
        # Render data
        if self.data:
            if type(self.data)==type({}):
                pass
            else:
                n=1
                for row in self.data:
                    s+=["<tr class='row%d'>"%(n%2+1)]
                    if self.enumerate:
                        s+=["<td align='right'>%d</td>"%n]
                    n+=1
                    for c,d in zip(self.columns,row):
                        s+=[c.format_html(d)]
                        c.contribute_data(d)
                    s+=["</tr>"]
        # Render totals
        if self.has_total:
            s+=["<tr>"]
            if self.enumerate:
                s+=["<td></td>"]
            for c in self.columns:
                s+=[c.format_html_total()]
            s+=["</tr>"]
        s+=["</tbody>"]
        s+=["</table>"]
        return "\n".join(s)
    ##
    ## Return CSV representation of table
    ##
    def to_csv(self):
        f=cStringIO.StringIO()
        writer=csv.writer(f)
        if self.enumerate:
            writer.writerow(["#"]+[c.title for c in self.columns])
        else:
            writer.writerow([c.title for c in self.columns])
        if self.data:
            if type(self.data)==type({}):
                pass
            else:
                if self.enumerate:
                    n=1
                    for row in self.data:
                        writer.writerow([n]+list(row))
                else:
                    for row in self.data:
                        writer.writerow(row)
        return f.getvalue()
##
##
##
class SimpleReport(ReportApplication):
    ##
    ## Returns Report object
    ##
    def get_data(self,**kwargs):
        return Report()
    ##
    ## Render HTML
    ##
    def report_html(self,**kwargs):
        return self.get_data(**kwargs).to_html()
    ##
    ## Render CSV
    ##
    def report_csv(self,**kwargs):
        return self.get_data(**kwargs).to_csv()
    ##
    ## Shortcut to generate Report from dataset
    ##
    def from_dataset(self,title,columns,data,enumerate=False):
        r=Report()
        r.append_section(TextSection(title=title))
        r.append_section(TableSection(columns=columns,data=data,enumerate=enumerate))
        return r
    ##
    ## Shortcut to generate Report from SQL query
    ##
    def from_query(self,title,columns,query,params=[],enumerate=False):
        return self.from_dataset(title=title,columns=columns,data=self.execute(query,params),enumerate=enumerate)
