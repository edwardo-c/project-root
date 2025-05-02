class Customer():
    def __init__(self, acct_num, norm, orig, 
                 match_type):
        self.acct_num = acct_num
        self.norm = norm
        self.orig = orig
        self.match_type = match_type

    def __repr__(self):
        return f"Customer: {self.orig}"