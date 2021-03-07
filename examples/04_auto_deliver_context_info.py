from lk_lambdex import lambdex


class AAA:
    ooo = 'ooo'

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def mmm(self, ppp):
        qqq = lambdex((), '''
            # lambdex can auto detect the context variables
            print(ppp)
            print(self.ooo)
        ''')
        qqq()


aaa = AAA()
aaa.mmm('ppp')
