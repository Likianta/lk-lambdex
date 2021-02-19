from lk_lambdex import lambdex


class AAA:
    ooo = 'ooo'

    # noinspection PyMethodMayBeStatic
    def mmm(self, ppp):
        # print(globals())
        #   {
        #       '__name__': '__main__',
        #       '__doc__': None,
        #       '__package__': None,
        #       '__loader__': <_frozen_importlib_external.SourceFileLoader
        #           object at 0x0000017626F82FD0>,
        #       '__spec__': None,
        #       '__annotations__': {},
        #       '__builtins__': <module 'builtins' (built-in)>,
        #       '__file__': __file__,
        #       '__cached__': None,
        #       'AAA': <class '__main__.AAA'>,
        #       'aaa': <__main__.AAA object at 0x0000017627285FD0>
        #   }
        # print(locals())
        #   {
        #       'self': <__main__.AAA object at 0x0000017627285FD0>,
        #       'ppp': 'ppp'
        #   }
        
        qqq = lambdex((locals()), '''
            print(ppp)
            print(self.ooo)
        ''')
        qqq()


aaa = AAA()
aaa.mmm('ppp')
