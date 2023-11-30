# -*- coding: utf-8 -*- 
import pickle
import copy
import re
from collections import defaultdict

class Bigram:
    def __init__(self,file,enc = 'utf-8', mode = 50000):
        # self.raw = open(file,encoding = enc)
        self.raw = open(file,encoding = enc)
        self.raw_ = open("KCC150_Korean_sentences_UTF8.txt",encoding = enc)
        # self.raws = [self.raw,self.raw_]
        self.raws = [self.raw_]
        self.mode = mode
    def bigram(self,text):
        bi = []
        # text = 
        text='#'+text+'@'
        for i in range(len(text)-1):
            bi.append(text[i:i+2])
        # print(bi)
        # exit()
        return bi
    
    def ngram(self,stop_flag=False):
        self.bi = defaultdict(int)
        self.uni = defaultdict(int)
        for raw in self.raws:
            for index,text in enumerate(raw):
                text = text.strip()
                
                for i in range(2):
                    if i == 0:
                        bitk = self.bigram(text)
                    else:
                        text = text.replace('.','').replace('?','').replace('!','')
                        bitk = self.bigram(text)
                    for bi_ in bitk:
                        self.bi[bi_] += 1
                        self.uni[bi_[0]] += 1
                if (index+1) == self.mode and stop_flag:
                    raw.close()
                    break
            if not stop_flag:
                raw.close()
    def prob(self):
        biprob = {}
        uniprob = {}
        self.ngram(stop_flag=True)
        for k,v in self.bi.items():
            biprob[k] = v / self.uni[k[0]]
        for k,v in self.uni.items():
            uniprob[k] = v / sum(self.uni.values())
        # print(biprob)
        with open('sbigram.pkl','wb') as f:
            pickle.dump(biprob,f)
        with open('sunigram.pkl','wb') as f:
            pickle.dump(uniprob,f)

class Ngram:
    def __init__(self,file,enc = 'utf-8', mode = 50000, n = 2):
        self.raw = open(file,encoding = enc)
        self.raw_ = open("KCC150_Korean_sentences_UTF8.txt",encoding = enc)
        self.raws = [self.raw,self.raw_]
        # self.raws = [self.raw]
        self.mode = mode
        self.n = n
    def _ngram(self,text):
        bi = []
        # text = 
        text='#'+text+'@'
        for i in range(len(text)-self.n-1):
            bi.append(text[i:i+self.n])
        # print(bi)
        # exit()
        return bi

    def _ngram_prev(self,text):
        text = list(text)
        text.reverse()
        text = ''.join(text)
        bi = []
        # text = 
        text='#'+text+'@'
        for i in range(len(text)-self.n-1):
            bi.append(text[i:i+self.n])
        # print(bi)
        # exit()
        return bi
    
    def ngram(self,stop_flag=False):
        self.ni = defaultdict(int)
        self.pre = defaultdict(int)
        self.space = defaultdict(int)
        self.pre_space = defaultdict(int)
        self.nip = defaultdict(int)
        self.prep = defaultdict(int)
        # for i in range(2):
        for raw in self.raws:
            for index,text in enumerate(raw):
                text = text.strip()
                text = re.sub(" +"," ",text)
               
                for i in range(2):
                    if i == 0:
                        bitk = self._ngram(text)
                        bitkp = self._ngram_prev(text)
                    else:
                        text = text.replace('.',' ').replace('?',' ').replace('!',' ').replace(',',' ')
                        text = text.strip()
                        text = re.sub(" +"," ",text)
                        bitk = self._ngram(text)
                        bitkp = self._ngram_prev(text)
                    for bi_ in bitk:
                        self.ni[bi_] += 1
                        self.pre[bi_[:self.n-1]] += 1

                        # if bi_[1] == " ":
                            # print(bi_)
                        self.space[bi_] += 1
                        self.pre_space[bi_[0]+bi_[2]] += 1
                    for bi_ in bitkp:
                        self.nip[bi_] += 1
                        self.prep[bi_[:self.n-1]] += 1

                if (index+1) == self.mode and stop_flag:
                    raw.close()
                    break
            if not stop_flag:
                raw.close()
    def prob(self):
        biprob = {}
        biprobp = {}
        uniprob = {}
        self.ngram(stop_flag=False)
        c = 0
        for k,v in self.ni.items():
            # if c == 2:
            #     print(k,k[:self.n-1])
                
            biprob[k] = v / self.pre[k[:self.n-1]]
            c += 1
        for k,v in self.nip.items():
            # if c == 2:
            #     print(k,k[:self.n-1])
                
            biprobp[k] = v / self.prep[k[:self.n-1]]
            c += 1
        # for k,v in self.pre.items():
        #     uniprob[k] = v / sum(self.pre[].values())
        # print(biprob)
        with open('{}_gram.pkl'.format(self.n),'wb') as f:
            pickle.dump(biprob,f)
        with open('{}_gram_prev.pkl'.format(self.n),'wb') as f:
            pickle.dump(biprobp,f)
        space_prob = {}
        with open('space.pkl','wb') as f:
            test = defaultdict(int)
            for k,v in self.space.items():
                # print(k,len(k))
                # print(v)
                test[v] += 1
                if k == '안' + ' ' + '내':
                    print(v,self.pre_space[k[0]+k[2]])
                # if v == self.pre_space[k[0]+k[2]] or v == self.pre_space[k[0]+k[2]]:
                #     space_prob[k] = 0.00000001
                #     continue
                space_prob[k] = v / self.pre_space[k[0]+k[2]]
                
                # print(space_prob[k],v,self.pre_space[k[0]+k[2]])
            pickle.dump(space_prob,f)
            # print(test)
        # with open('sunigram.pkl','wb') as f:
        #     pickle.dump(uniprob,f)

class SentenceSplit:
    def __init__(self,thread_hold=0.3):
        with open('sbigram.pkl','rb') as f:
            self.biprob = pickle.load(f)
        with open('sunigram.pkl','rb') as f:
            self.uniprob = pickle.load(f)
        self.thread_hold = thread_hold
    
    def split(self,string):
        temp = 1.0
        result = list(copy.deepcopy(string))
        text = string
        flag = False
        for t in range(len(text)-1):
            bi = text[t:t+2]
            if bi in self.biprob:
                if bi[1] + '@' in self.biprob:
                    end_prob =  self.biprob[bi]*self.biprob[bi[1]+'@']
                    print(bi[1],end_prob)
                    if end_prob > self.thread_hold:
                        result[t+1] = result[t+1] + '@'
                        flag = True
        return self.split_result(result)
    
    def split_result(self,text):
        temp = ''.join(text)
        temp = temp.replace('@.@','.@')
        result = []
        for t in temp.split('@'):
            tstrip = t.strip()
            if tstrip != '':
                result.append(tstrip)
        return tuple(result)
            
if __name__ == '__main__':
    from hanspell import spell_checker
    from tqdm import tqdm
    import pandas as pd
    t = "지금까지 본 드라마 중 최악의 드라마네요스토리 연출 연기아이구정일우 씨가 아깝다 다음엔 가려가며 출연하세요"
    # print(SentenceSplit(thread_hold=0.003).split(t))
    # exit()
    data = pd.read_csv('noht_train_autocorrect.csv')
    with open('result_file.txt') as f:
        pbar = tqdm(total=len(f.readlines()))
        f.seek(0)
        with open('result_file_spell.txt','w') as ff:
            for l in f:
                l = l.strip()
                if len(l.split()) > 3:
                #    l = spell_checker.check(l).as_dict()["checked"]
                    ff.write(l+'\n')    
                pbar.update(1)
                
            # data = data.dropna()
            # f = data.loc[:,["text"]].values
            # import numpy as np
            # f = np.reshape(f,(f.shape[0]))
            
            # for l in f:
            #     l = l.strip()
            #     if len(l.split()) > 3:
            #     #    l = spell_checker.check(l).as_dict()["checked"]
            #         ff.write(l+'\n')
            #     pbar.update(1)
        pbar.close()
    bigram = Bigram('result_file_spell.txt',mode=5000000)
    bigram.prob()

    bigram = Ngram('result_file_spell.txt',mode=5000000,n = 3)
    bigram.prob()
    
    exit()
    text = '나는 밥을 먹고 학교에 갔다. 배가 고파 피자도 먹었다.' 
    
    # text ='왜 그런 잔인한, 잔인하고 끔찍한 자해 행위를 사람들 앞에서 서슴없이 하는 거죠? 산으로 도망친 걸 보니 너도 천주학장이로구나! 나 집에 보내줘! 나는 밥을 먹고 학교에 갔다'
    text = '''윤석열 대통령이 주재한 국무회의에서 양곡관리법 개정안에 대한 재의요구, 거부권이 의결됐습니다. 윤 대통령은 양곡법 개정안이 "농업 생산성을 높이고 농가 소득을 높이려는 정부의 농정 목표에도 반하고, 농업인과 농촌 발전에도 전혀 도움이 되지 않는 전형적인 포퓰리즘 법안"이라고 말했습니다. 윤 대통령은 오늘(4일) 용산 대통령실에서 국무회의를 주재하고 "정부는 이번 법안(양곡법 개정안)의 부작용에 대해 국회에 지속적으로 설명해 왔지만, 제대로 된 토론 없이 국회에서 일방적으로 통과시켜 매우 유감스럽게 생각한다"고 밝혔습니다. 이어 "이번 양곡관리법 개정안은 시장의 쌀 소비량과 관계없이 남는 쌀을 정부가 국민의 막대한 혈세를 들여서 모두 사들여야 한다는 '남는 쌀 강제 매수법'"이라고 규정했습니다. 그러면서 전문가 연구 결과를 인용해 "이렇게 쌀 생산이 과잉되면 오히려 궁극적으로 쌀의 시장 가격을 떨어뜨리고 농가 소득을 더욱 불안정하게 만들 것"이라고 했습니다. 윤 대통령은 "법안 처리 이후 40개의 농업인 단체가 양곡관리법 개정안에 대해 전면 재논의를 요구했고, 관계부처와 여당도 현장의 목소리를 경청하고 검토해서 재의요구권 행사를 건의했다"고 여론수렴 과정을 설명했습니다. 오늘 국무회의에서 의결된 양곡법 개정안 재의요구를 윤 대통령이 재가하면, 지난 2016년 이후 7년 만이자 역대 67번째 거부권 행사가 됩니다.'''
    # from konlpy.tag import Kkma
    # k = Kkma()
    text = '''한국CXO연구소 오일선 연구소장은 “지난해는 그룹 총수들도 주식평가액 하락이라는 혹한기를 피해가지 못했다”며 “그룹 총수들은 경영권 방어를 위해서 지분을 쥐고 있는 경우가 많지만, 개미와 기관 투자자 중에는 주식을 급하게 처분해 현금 자산을 확보해야 하는 경우가 많다는 점을 감안하면 지난해에는 그야말로 주식으로 인한 손실 폭이 큰 한 해로 기록됐다"고 분석했다.'''
    text = '''국회 국토교통위원회의 28일 전체회의에서 여야는 전세 사기 사태의 원인과 피해 지원 특별법의 실효성 등을 두고 공방을 벌였다.

여당은 문재인 정부 때 도입한 '임대차 3법'이 부동산 시장 불안정성을 촉발하며 이번 사태를 초래했다고 주장한 반면, 야당은 이명박 정부 때부터 장려한 전세 보증 대출의 허점을 악용한 사건이라고 반박했다.

국민의힘 엄태영 의원은 "지난 정부 때 무리하게 밀어붙인 임대차 3법이 전세 사기에 판을 깔아줬다는 전문가들의 의견이 있다"면서 "이 말이 100% 맞지 않더라도 일말의 책임감을 느껴야 할 텐데 (민주당은) 반성과 사과나 흔한 유감 표명 하나 없다"고 말했다.

회의에 출석한 원희룡 국토교통부 장관도 "매매가격이 폭등하던 시절 임대차 3법을 일방적으로 처리하고 시장에서 이 충격을 흡수할 여건이 안 됐는데 시행함으로써 전셋값을 폭등시킨 분명한 계기가 됐다"고 지적했다.

이에 대해 민주당 허영 의원은 "정부는 2008년 이후 전세보증금 대출 제도를 시행하면서 전세 정책을 장려해 왔다"라며 "정부 정책의 허점을 이용한 전세 사기이고 깡통전세로 인한 피해"라고 반박했다.

허 의원은 또 "청년에 대해서는 대출 우대 정책을 통해 월세보다 전세를 더 선호하게끔 만들어 전셋값이 인상되는 효과가 발생했다"고 지적했다.

특별법의 전세 사기 피해자 구제 방안을 놓고도 여야는 충돌했다.

정부·여당의 특별법안은 전세 사기 피해자의 주택이 경매로 넘어갔을 때 우선매수권을 부여한다는 내용이지만, 한국자산관리공사(캠코) 등 채권 매입기관이 보증금 반환 채권을 사들여 피해자를 먼저 지원토록 해야 한다는 게 야당의 주장이다.

민주당 맹성규 의원은 "정부안에는 피해자들에 대한 보증금 반환 방안이 전혀 없다"고 지적했다.

정의당 심상정 의원도 전세사기 피해자 요건에 해당해야 지원을 받을 수 있는 여당 안을 두고 "피해자 걸러내기 법이냐는 문제 제기가 있다. 조건이 매우 협소하다"고 비판했다.

이에 대해 원 장관은 "모든 사기 피해는 평등하다"며 채권 매입을 통한 보증금 반환 방안을 받아들일 수 없다고 밝힌 뒤 "보증금 직접 지급에 대해서는 (불가하다는) 확고한 원칙을 지킬 수밖에 없다"고 설명했다.

국토위는 대체토론 후 정부·여당이 마련해 국민의힘 김정재 의원이 대표 발의한 '전세 사기 피해자 지원 및 주거안정 특별법', 더불어민주당 조오섭 의원의 '주택 임차인의 보증금 회수 및 주거안정 지원 특별법', 정의당 심상정 의원의 '임대보증금 미반환주택 임차인 보호 특별법'까지 3건을 의결, 법안심사 소위로 넘겼다.

국토위는 내달 1일 법안심사 소위를 거쳐 2일 전체회의를 다시 열어 이들 법안을 의결할 계획이며, 이르면 5월 초 국회 본회의에서 의결될 것으로 보인다.

이와 함께 전세 사기 대책의 일환인 민간임대주택에 관한 특별법 개정안과 공인중개사법 개정안 3건도 이날 전체회의에 상정됐다.

공인중개사법 개정안은 부동산 거래 질서 교란 행위에 대한 신고센터 역할을 확대하고, 공인중개사 자격증·중개사무소 등록증을 대여, 알선하는 행위의 처벌과 자격 취소 요건을 구체화했다.'''
    text = text + text + text + text+ text + text + text
    # print(k.pos('왜 그런 잔인한, 잔인하고 끔찍한 자해 행위를 사람들 앞에서 서슴없이 하는 거죠'))
    # print(k.pos('산으로 도망친 걸 보니 너도 천주학장이로구나'))
    # print(k.pos('나 집에 보내줘'))
    # print(k.pos('나는 밥을 먹고 학교에 갔다'))
    import time
    start = time.time()
    ss = SentenceSplit()
    
    res = ss.split(text)
    print(res)
    print(time.time()-start)
    exit()
    temp = 1.0
    # temp2 = 1.0
    import copy
    result = list(copy.deepcopy(text))
    flag = False
    for t in range(len(text)-1):
        bi = text[t:t+2]
        if bi in biprob:
            print(bi,biprob[bi],bi[1],end=',')
            if bi[1] + '@' in biprob:
                # print(temp*biprob[bi]*biprob[bi[1]+'@'])
                end_prob =  biprob[bi]*biprob[bi[1]+'@']
                print(end_prob)
                
                if end_prob > 0.3:
                    result[t+1] = result[t+1] + '@'
                    flag = True
            print()
            # else:
                # print(bi[1]+'@',0.0)
        
        if flag:
            temp = 1.0
            flag = False
        elif bi in biprob:
            temp = biprob[bi]
        else:
            # print(bi)
            if bi[1] in uniprob: #and bi[1]
                temp = uniprob[bi[1]]# * uniprob[bi[1]]
    import re
    result = ''.join(result)
    result = result.replace('@.@','.@')
    for l in result.split('@'):
        print(l.strip())
