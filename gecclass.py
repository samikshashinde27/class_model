from datetime import date, datetime, timedelta


from gec_common import funcation as fn
  
class tender:
    def __init__(self):
        self.types: str = None
        self.movie_title: str = None # character varying(4000)
        self.country_code : str = None #character varying(4000) , class performance_country
        self.user_score: float = 0.00 #bigint,
        self.release_date: datetime = None # date,
        self.directore_name: str = None #text COLLATE pg_catalog."default",
        self.duration: str = None #character varying(500) COLLATE pg_catalog."default",
        self.writer_name: str = None #character varying(500) COLLATE pg_catalog."default",     
        self.status: str = None #character varying(500),
        self.original_language: str = None #character varying(500),   
        self.overview: str = '' #text
        self.sub_url: str = None #character varying(4000),
        self.budget : float  = 0.00 #  numeric(15,2) DEFAULT 'NULL::numeric',
        self.revenue : float  = 0.00 #  numeric(15,2) DEFAULT 'NULL::numeric',
        self.reviews :int = 0
        
    def tender_cleanup(self):
            
        if self.types == '':
            self.types = None
                
        if self.movie_title == '':
            self.movie_title = None
            
        if self.country_code == '':
            self.country_code = None
            
        if self.release_date == '':
            self.release_date = None
            
        if self.directore_name == '':
            self.directore_name = None
            
        if self.duration == '':
            self.duration = None
            
        if self.writer_name == '':
            self.writer_name = None
            
        if self.status == '':
            self.status = None
            
        if self.original_language == '':
            self.original_language = None
            
        if self.overview == '':
            self.overview = None
            
        if self.sub_url == '':
            self.sub_url = None

        if type(self.user_score) is float:
            self.user_score = float("%.2f" % self.user_score)
        elif type(self.user_score) is int:
            self.user_score = float(self.user_score)
        else:
            self.user_score = 0.00

        if type(self.budget) is float:
            self.budget = float("%.2f" % self.budget)
        elif type(self.budget) is int:
            self.budget = float(self.budget)
        else:
            self.budget = 0.00

        if type(self.revenue) is float:
            self.revenue = float("%.2f" % self.revenue)
        elif type(self.revenue) is int:
            self.revenue = float(self.revenue)
        else:
            self.revenue = 0.00

        if type(self.reviews) is int:
            self.reviews = self.reviews
        else:
            self.reviews = 0
