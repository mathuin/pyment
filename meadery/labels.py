from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import BaseDocTemplate, Paragraph, Frame, PageTemplate, FrameBreak, Table, Image
from pyment.settings import SITE_NAME, BREWER_NAME, BREWER_LOCATION
from cStringIO import StringIO
from .models import Batch
from django.http import HttpResponse


class RotatedTable(Table):
    """
    Rotating tables makes rotating labels possible.
    """
    def wrap(self, availWidth, availHeight):
        h, w = Table.wrap(self, availHeight, availWidth)
        return w, h

    def draw(self):
        self.canv.translate(self._height, 0)
        self.canv.rotate(90)
        Table.draw(self)


class Sheet:
    """
    Base class for sheets of labels.
    """
    def __init__(self, buffer=None, debug=False):
        # Buffer must be set!
        if buffer is None:
            raise ValueError('Buffer argument is required')
        else:
            self.buffer = buffer
        self.debug = debug

        # Label parameters are for Avery 6572.
        # TODO: allow this to be set via options or some other way.
        # ... a horrible part of me is considering adding a model for label sheets.
        self.width = 612
        self.height = 792
        self.top_margin = 36
        self.bottom_margin = 36
        self.left_margin = 9
        self.right_margin = 9
        self.rows = 5
        self.cols = 3
        self.row_gutter = 0
        self.col_gutter = 9

        # Calculate label width and height.
        self.labelw = int((self.width - self.left_margin - self.right_margin - (self.cols - 1)*self.col_gutter) / self.cols)
        self.labelh = int((self.height - self.top_margin - self.bottom_margin - (self.rows - 1)*self.row_gutter) / self.rows)

        # Get sample style sheet from styles.
        self.styles = getSampleStyleSheet()
        self.style = self.styles['Normal']

        # Create document from base template.
        self.doc = BaseDocTemplate(self.buffer, pagesize=(self.width, self.height))

        # Construct page template of "frames".  Each frame contains one label.
        self.framelist = [(self.left_margin+y*(self.col_gutter+self.labelw), self.height-self.bottom_margin-self.labelh-x*(self.row_gutter+self.labelh), self.labelw, self.labelh) for x in xrange(self.rows) for y in xrange(self.cols)]
        self.doc.addPageTemplates([PageTemplate(frames=[Frame(a, b, c, d, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary=(1 if self.debug else 0)) for (a, b, c, d) in self.framelist])])

    def __call__(self, data):
        # table style for outer table is middle center
        ts = [('ALIGN', (0, 0), (0, 0), 'CENTER'), ('VALIGN', (0, 0), (0, 0), 'MIDDLE')]
        # labels are list of tables containing actual rendered records
        Sheet = [Table([[record.render(self)]], style=ts, colWidths=self.labelw, rowHeights=self.labelh) for record in data]
        self.doc.build(Sheet)


class Label:
    """
    Base class for labels.

    Includes constants like health warnings and default flavor texts.

    Everything else comes from the batch.
    """
    # absolute constants
    # 27 CFR sec 16.21 Mandatory label information - health warning
    health_warning_text = "<b>GOVERNMENT WARNING:</b>  (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."
    bottled_text = 'Bottled by {}, <br /> {}'.format(BREWER_NAME, BREWER_LOCATION)
    flavor_text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
    # border
    border_width = 2
    # inset
    inset = 1

    # init
    def __init__(self, seq, batch, debug=False):
        self.seq = '{}{}'.format(batch.batchletter, seq+1)
        self.batch = batch
        self.debug = debug

    # default render
    def render(self, sheet):
        # make a table filling width and height here
        tabledata = [[self.batch.title, ''],
                     ['', ''],
                     [self.batch.brewname, self.seq]]
        tablestyle = [('SPAN', (0, 0), (1, 0)),
                      ('ALIGN', (0, 0), (1, 0), 'CENTER'),
                      ('VALIGN', (0, 0), (1, 0), 'TOP'),
                      ('SPAN', (0, 1), (1, 1)),
                      ('ALIGN', (0, 1), (1, 1), 'CENTER'),
                      ('VALIGN', (0, 1), (1, 1), 'MIDDLE'),
                      ('ALIGN', (0, 2), (0, 2), 'LEFT'),
                      ('ALIGN', (1, 2), (1, 2), 'RIGHT'),
                      ('VALIGN', (0, 2), (1, 2), 'BOTTOM')]
        return Table(tabledata, style=tablestyle)


class Brand(Label):
    """
    Example of a brand label.

    27 CFR S4.32 - mandatory label information

    brand label: (first three same size/kind lettering)
      brand name (S4.33)
      distinctive/fanciful (S4.34)
      class/type (S4.34)
      alcohol content (S4.36)
        Alcohol __% by volume or alc. __% by vol.
    """
    abv_format = "alc. %0.1f%% by vol."
    # XXX: consider abv_style
    abv_font = 'Helvetica'
    abv_size = 9
    # XXX: consider brand_style
    brand_size = 12
    # XXX: consider footer_style
    footer_font = 'Helvetica-Bold'
    footer_size = 9

    def __init__(self, seq, batch, holiday=None):
        Label.__init__(self, seq, batch)
        # JMT: get from batch eventually
        self.holiday = holiday
        if self.batch.all_natural():
            self.class_type_name = 'Natural Honey Wine'
        else:
            self.class_type_name = 'Honey Wine'

    def render(self, sheet):
        realwidth = sheet.labelw - 2*Label.border_width - 4*Label.inset
        realheight = sheet.labelh - 2*Label.border_width - 4*Label.inset

        bottabledata = [[self.batch.brewname, Brand.abv_format % self.batch.abv, self.seq]]
        minbotwidths = [stringWidth(self.batch.brewname, Brand.footer_font, Brand.footer_size), stringWidth(Brand.abv_format % self.batch.abv, Brand.abv_font, Brand.abv_size), stringWidth(self.seq, Brand.footer_font, Brand.footer_size)]
        botwidths = [w * realheight / sum(minbotwidths) for w in minbotwidths]
        bottablestyle = [('ALIGN', (0, 0), (0, 0), 'LEFT'),
                         ('LEFTPADDING', (0, 0), (0, 0), 3),
                         ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                         ('RIGHTPADDING', (2, 0), (2, 0), 3),
                         ('VALIGN', (0, 0), (2, 0), 'BOTTOM'),
                         ('TOPPADDING', (0, 0), (2, 0), 3),
                         ('BOTTOMPADDING', (0, 0), (2, 0), 3),
                         ('FONT', (0, 0), (0, 0), Brand.footer_font),
                         ('FONT', (1, 0), (1, 0), Brand.abv_font),
                         ('FONT', (2, 0), (2, 0), Brand.footer_font),
                         ('FONTSIZE', (0, 0), (0, 0), Brand.footer_size),
                         ('FONTSIZE', (1, 0), (1, 0), Brand.abv_size),
                         ('FONTSIZE', (0, 0), (2, 0), Brand.footer_size),
                         ]
        if self.debug:
            bottablestyle.append(('GRID', (0, 0), (-1, -1), 1, colors.blue))
        bottable = Table(bottabledata, style=bottablestyle, colWidths=botwidths)
        bottable._calc(realheight, realwidth)

        tabledata = [[SITE_NAME],
                     [self.holiday],
                     [self.batch.title],
                     [self.batch.appellation()],
                     [self.class_type_name],
                     [bottable]]
        tablestyle = [('ALIGN', (0, 0), (0, -1), 'CENTER'),
                      ('VALIGN', (0, 0), (0, 2), 'TOP'),
                      ('VALIGN', (0, 3), (0, -2), 'BOTTOM'),
                      ('VALIGN', (0, -1), (0, -1), 'TOP'),
                      ('FONTSIZE', (0, 0), (0, 5), Brand.brand_size),
                      ]
        if self.debug:
            tablestyle.append(('GRID', (0, 0), (-1, -1), 1, colors.green))
        if Label.border_width > 0:
            tablestyle.append(('BOX', (0, 0), (-1, -1), Label.border_width, colors.red))

        minrowheights = [Brand.brand_size, Brand.brand_size, Brand.brand_size, Brand.brand_size, Brand.brand_size, bottable._height]
        rowheights = [h * sheet.labelw / sum(minrowheights) for h in minrowheights]

        return RotatedTable(tabledata, style=tablestyle, colWidths=realheight, rowHeights=rowheights)


class Back(Label):
    """
    Example of a back label.

    27 CFR S4.32 - mandatory label information

    name and address (S4.35)
      Bottled by Your Name, Anywhere, USA
    net contents (S4.37)
      If not authorized metric standard as in S4.72, on front
      1 liter (33.8 fl. oz.) (can be on back)
    """
    flavor_size = 6
    health_size = 6
    bottled_size = 8
    net_contents_text = "1 liter"
    # XXX: consider net_contents_style
    net_contents_font = 'Helvetica'
    net_contents_size = 9
    footer_font = 'Helvetica-Bold'
    footer_size = 9

    def __init__(self, seq, batch, flavor_text=Label.flavor_text):
        Label.__init__(self, seq, batch)
        self.flavor_text = flavor_text

    def render(self, sheet):
        realwidth = sheet.labelw - 2*Label.border_width - 4*Label.inset
        realheight = sheet.labelh - 2*Label.border_width - 4*Label.inset

        flavor_style = ParagraphStyle('flavor')
        flavor_style.fontSize = self.flavor_size
        flavor_style.leading = self.flavor_size+1
        flavor_style.alignment = TA_JUSTIFY

        flavor_text_paragraph = Paragraph(self.flavor_text, flavor_style)
        flavorw, flavorh = flavor_text_paragraph.wrap(realheight, realwidth)

        bottled_style = ParagraphStyle('bottled')
        bottled_style.fontSize = self.bottled_size
        bottled_style.leading = self.bottled_size+2
        bottled_style.alignment = TA_CENTER

        bottled_paragraph = Paragraph(Label.bottled_text, bottled_style)
        bottledw, bottledh = bottled_paragraph.wrap(realheight, realwidth)

        health_style = ParagraphStyle('health')
        health_style.fontSize = self.health_size
        health_style.leading = self.health_size+1
        health_style.alignment = TA_JUSTIFY

        health_warning_paragraph = Paragraph(Label.health_warning_text, health_style)
        healthw, healthh = health_warning_paragraph.wrap(realheight, realwidth)

        bottabledata = [[self.batch.brewname, self.net_contents_text, self.seq]]
        minbotwidths = [stringWidth(self.batch.brewname, Back.footer_font, Back.footer_size), stringWidth(self.net_contents_text, self.net_contents_font, self.net_contents_size), stringWidth(self.seq, Back.footer_font, Back.footer_size)]
        botwidths = [w * realheight / sum(minbotwidths) for w in minbotwidths]
        bottablestyle = [('ALIGN', (0, 0), (0, 0), 'LEFT'),
                         ('LEFTPADDING', (0, 0), (0, 0), 3),
                         # stupid metrics
                         ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                         ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
                         ('RIGHTPADDING', (2, 0), (2, 0), 3),
                         ('VALIGN', (0, 0), (2, 0), 'BOTTOM'),
                         ('TOPPADDING', (0, 0), (2, 0), 3),
                         ('BOTTOMPADDING', (0, 0), (2, 0), 3),
                         ('FONT', (0, 0), (0, 0), Back.footer_font),
                         ('FONT', (1, 0), (1, 0), self.net_contents_font),
                         ('FONT', (2, 0), (2, 0), Back.footer_font),
                         ('FONTSIZE', (0, 0), (0, 0), Back.footer_size),
                         ('FONTSIZE', (1, 0), (1, 0), self.net_contents_size),
                         ('FONTSIZE', (2, 0), (2, 0), Back.footer_size),
                         ]
        if self.debug:
            bottablestyle.append(('GRID', (0, 0), (-1, -1), 1, colors.blue))
        bottable = Table(bottabledata, style=bottablestyle, colWidths=botwidths)
        bottable._calc(realheight, realwidth)

        tabledata = [[flavor_text_paragraph],
                     [bottled_paragraph],
                     [health_warning_paragraph],
                     [bottable]]
        tablestyle = [('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                      ('VALIGN', (0, 0), (0, -2), 'MIDDLE'),
                      ('VALIGN', (0, -1), (0, -1), 'TOP'),
                      ('FONTSIZE', (0, 0), (0, 0), self.flavor_size),
                      ('FONTSIZE', (0, 1), (0, 1), self.bottled_size),
                      ('FONTSIZE', (0, 0), (0, 0), self.health_size),
                      ]
        if self.debug:
            tablestyle.append(('GRID', (0, 0), (-1, -1), 1, colors.green))
        if Label.border_width > 0:
            tablestyle.append(('BOX', (0, 0), (-1, -1), Label.border_width, colors.red))

        minrowheights = [flavorh, bottledh, healthh, bottable._height]
        rowheights = [h * sheet.labelw / sum(minrowheights) for h in minrowheights]

        return RotatedTable(tabledata, style=tablestyle, colWidths=realheight, rowHeights=rowheights)
