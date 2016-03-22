from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Table
from pyment.settings import SITE_NAME, BREWER_NAME, BREWER_LOCATION


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
    bottled_text = 'Bottled by {0}, <br /> {1}'.format(BREWER_NAME, BREWER_LOCATION)
    # border
    border_width = 2
    # inset
    inset = 1

    # init
    def __init__(self, seq, batch, debug=False):
        self.seq = '{0}{1}'.format(batch.batchletter, seq+1)
        self.batch = batch
        self.debug = debug

    # default render
    def render(self, sheet):
        # make a table filling width and height here
        tabledata = [[SITE_NAME, ''],
                     [self.batch.title, ''],
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
