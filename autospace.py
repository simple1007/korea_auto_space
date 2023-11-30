# -*- coding: utf-8 -*- 
import pickle
import copy
import re
# def load_bigram():
#     with open('bigram.pkl','rb') as f:
#         bigram = pickle.load(f)
#     return bigram

# def load_unigram():
#     with open('unigram.pkl','rb') as f:
#         unigram = pickle.load(f)
#     return unigram

# bigram = load_bigram()
# unigram = load_unigram()

# def get_bi_rbi(text,t):
#     bi = text[t:t+2]
#     rbi = text[t+1:t+3]

#     return bi, rbi

# def autospace(text):
#     result = list(copy.deepcopy(text))
#     t = 0
#     while True:
#         if text[t]+' ' in bigram and ' '+text[t+1] in bigram:
#             prob = bigram[text[t]+' ']
#             rprob = bigram[' '+text[t+1]]
#             if ((prob+rprob)/2) >= 0.28:
#                 result[t] = result[t] + ' '
#                 text = ''.join(result)
#                 result = list(copy.deepcopy(text))
#         t += 1
#         if (t+1) >= (len(text)-1):
#             break
#     return ''.join(result)

class AutoSpace:
    def __init__(self,temp=0.28):
        self.bigram = self.load_bigram()
        self.unigram = self.load_unigram()
        self.trigram = self.load_trigram()
        self.trigram_prev = self.load_trigram_prev()
        self.space = self.load_space()
        self.temp = temp

    def load_trigram_prev(self):
        with open('3_gram_prev.pkl','rb') as f:
            bigram = pickle.load(f)
        return bigram
    def load_space(self):
        with open('space.pkl','rb') as f:
            bigram = pickle.load(f)
        return bigram        
    def load_trigram(self):
        with open('3_gram.pkl','rb') as f:
            bigram = pickle.load(f)
        return bigram
    
    def load_bigram(self):
        with open('sbigram.pkl','rb') as f:
            bigram = pickle.load(f)
        return bigram

    def load_unigram(self):
        with open('sunigram.pkl','rb') as f:
            unigram = pickle.load(f)
        return unigram

    def get_bi_rbi(self,text,t):
        bi = text[t:t+2]
        rbi = text[t+1:t+3]

        return bi, rbi

    def autospace(self,text):
        # text = text.replace("이다","이다 ")
        text = '#' + text
        result = list(copy.deepcopy(text))
        t = 1

        while True:
            if (t+1) >= (len(text)-1):
                break
            if text[t] == ' ':
                t+=1
                continue
            # print(t)
            # if text[t]+' ' in self.bigram and ' '+text[t+1] in self.bigram:
                # print(text[t:t+2] + ' ')
            tprob = 0
            trprob = 0
            rf = False
            f = False
            if t >= 0:
                # print(text[t+1]+"+"+text[t+1:t+1+2]+"+",end="ff")
                # print(text[t]+"+"+text[t-1:t+1]+"+")
                # print(text[t-1:t+1])
                if text[t-1:t+1] + ' ' in self.trigram:
                    tprob = self.trigram[text[t-1:t+1] + ' ']
                else:
                    tprob = 0.00001#self.bigram[text[t-1]+' ']
                    f = True
                
                rtk = list(text[t+1:t+1+2])
                rtk.reverse()
                rtk = ''.join(rtk)
                
                if rtk + ' ' in self.trigram_prev: 
                    trprob = self.trigram_prev[rtk+' ']
                else:
                    trprob = 0.00001
                    rf = True
                    # trprob = self.bigram[' '+text[t+1]]
            space = 0
            sf = False
            if text[t] + " " + text[t+1] in self.space:
                space = self.space[text[t] + " " + text[t+1]]
            else:
                space = 0.00001
                sf = True
            # print('#'+rtk+'#'+'#'+text[t-1:t+1]+"#"+"#"+text[t] + " " + text[t+1]+"#")
            # else:
            #     tprob = 0
            #     trprob = 0
            # if space == 0:
            #     t += 1
            #     continue
            if text[t]+' ' in self.bigram:
                prob = self.bigram[text[t]+' ']
            else:
                prob = 0.00001
                # prob = self.unigram[text[t]] * self.unigram[' ']
            
            if ' '+text[t+1] in self.bigram:
                rprob = self.bigram[' '+text[t+1]]
            else:
                rprob = 0.00001
                # rprob = self.unigram[' '] * self.unigram[text[t+1]]
            

            # if tprob == 0 and trprob == 0:
            #     res = (prob+rprob)/2
            #     # t += 1
            #     # continue
            # else:
                # res1 = (prob + tprob) / 2
                # res2 = (rprob + trprob) / 2
                # res = ((res1+res2) * 0.5 + (space*1.0)) / 3

            count = 3

            # if f:
            #     count -= 1
            # if rf:
            #     count -= 1
            # if sf:
            #     count -= 1
            res = (tprob*0.25)+(space*0.5)+(trprob*0.25) / 3
            # if count > 0:
            # res = (tprob*0.25)+(space*0.5)+(trprob*0.25) / count
            # if space >= 0.96:
            #     t += 1
            #     continue
            # else:
            #     res = 0.00000001
            # res = (tprob*0.275)+(space*0.45)+(trprob*0.275) / 3
            # count = 3
            # if rf:#rprob == 0.00001:
            # 	count -= 1
            # if f:#tprob == 0.00001:
            # 	count -= 1
            # if sf:#space == 0.00001:
            # 	count -= 1
            # if count != 0:
            # 	res = res / count
            # else:
            # 	res = 0.00001
            # print(res,space,text[t])
            # print(text[t],res)
            if res > self.temp:
            # if ((prob+rprob)/2) >= self.temp:
                # print((prob+rprob+tprob+trprob)/4)
                result[t] = result[t] + ' '
                text = ''.join(result)
                text = re.sub(' +',' ',text)
                result = list(copy.deepcopy(text))
            # else:
            #     if text[t]+' ' not in self.bigram:
            #         prob = self.unigram[' '] * ( self.unigram[text[t]] if text[t] in self.unigram else 0.000001 )
            #     else:
            #         prob = self.bigram[text[t]+' ']
                
            #     if ' '+text[t+1] not in self.bigram:
            #         rprob = self.unigram[' '] * ( self.unigram[text[t+1]] if text[t+1] in self.unigram else 0.000001 )#self.unigram[text[t+1]]
            #     else:
            #         rprob = self.bigram[' '+text[t+1]]

            #     if ((prob+rprob)/2) >= self.temp * 0.9:
            #         result[t] = result[t] + ' '
            #         text = ''.join(result)
            #         result = list(copy.deepcopy(text))
            t += 1
            
        return ''.join(result)[1:]

class SentenceSplit:
    def __init__(self,thread_hold=0.04):
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
                    # print(end_prob)
                    # print(bi[1],end_prob)
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
    text = '부족했다보는내내답답함만'#'이해하거나못하거나껄끄럽고'
    #text = "Mbc 왜이러나?장보리재미보니이드라마도또방향을돌리네처음엔신선해서봤는데이젠하다하다못해부모자식간에막장을 ,이런쓰레기드라마만들려고공부하는지,반성좀하십요.자식보기부끄럽겠네평점1점도아깝다"#"세명의남자가솔직한선희에게어장관리당하는내용찰지게후리는구나"
    #text = "졸리의 마력엔 어쩔수 없다는 걸 말하고 싶은 건가."
    
    #text = '''13일 카카오는 이와 같이 밝히며 스마트폰 첫 화면에서 즉각 친구들의 새소식을 접하고 카카오톡 메시지 전송까지 할 수 있는카카오홈과 함께 더 쉽고빠른 모바일 커뮤니케이션을 경험할 수 있을 것이라고 설명했다.'''
    #text = "나는밥을먹고학교에갔다."
    #text = '크루즈산업육성법은 이와 함께 전문인력 양성 등 크루즈산업의 체계적인 육성을 위한 인프라 구축 및 지원 방안도 담고 있다마리나항만법은 마리나항만 개발 사업의 신속성 및 효율성을 도모하는 개정안이다.'
    stk = SentenceSplit()
    res = stk.split(text)

    print(AutoSpace(temp=0.56).autospace(res[0]))
    print(AutoSpace(temp=0.56).autospace(res[1]))

    exit()

    from tqdm import tqdm
    autospace = AutoSpace(temp=0.56)
    with open("KCC150_Korean_sentences_UTF8.txt",encoding="utf-8") as f:
        with open("autospace_kcc_.txt","w",encoding="utf-8") as ff:
            count = 0
            for l in f:
                #l = l.strip()
                count += 1
            f.seek(0)
            with tqdm(total=count) as pbar:
                for l in f:
                    l = l.strip()
                    l = autospace.autospace(l)                                                                                                          
                    ff.write(l+"\n")
                    pbar.update(1)
    exit()



    # text = "잔인했다"
    # text = "아쉽기까지했다"#'나는밥을먹고학교에갔다.'
    #text = "심했다이해할"
    # text = '방사청은이번원가관리안내서를희망하는기업에무료로배포할예정이다.'
    # text = '통합보건교육은이대학만의특화된프로그램이다.'
    # text = "영화같음"
    #text = "재미없음"
    # text = "심했다이해할수없는영화"
    # text = "하이거스케일도완전작고스토리도아무영화에서아무거나갖다붙였네요시간아까워요"
    # print(AutoSpace(temp=0.52).autospace(text))
    # t = "지금까지 본 드라마 중 최악의 드라마네 요스토리 연출 연기아이구정일우 씨가 아깝다 다음엔 가려가며 출연하세요"
    exit()
    auto = AutoSpace(temp=0.56)
    while True:
      text = input("input:")
      print(auto.autospace(text))
    exit()
    #bigram = load_bigram()
    #unigram = load_unigram()
    # text = '세계금융시장이극심한공포에서잠시벗어났다.'
    # text = '나는밥을먹고학교에갔다.'#
    # text = '그런데 황희찬이다시1부로올라갈수도있다'
    # text = '방사청은이번원가관리안내서를희망하는기업에무료로배포할예정이다.'
    
    result = list(copy.deepcopy(text))
    t = 0
    temp = 0.2
    rtemp = 0.2
    # for t in range(len(text)-1):
    while True:#(t+1) <= (len(result)-1):
        # print(t)
        
        bi = text[t:t+2]
        rbi = text[t+1:t+3]
        print(bi,rbi)
        # if t == 0:
        #     bi1 = 1.0
        # bi1 = text[t+1:t+3]
        # print(bi)
        # if bi not in bigram or rbi not in bigram:
        #     # bip = unigram[bi[1]]
        #     temp = 0.2
        #     rtemp= 0.2
        #     t+=1
        #     continue
        # else:
        # bip = bigram[bi]
        # if t !=0:
        #     bi2 = bigram[bi]
        # rbip = bigram[bi[1]+text[t+2]]
        # print(text[t])
        if text[t]+' ' in bigram and ' '+text[t+1] in bigram:
            prob = bigram[text[t]+' ']
            spacep = temp * prob
            # print(text[t],text[t+1],text[t+2])
            rprob = bigram[' '+text[t+1]]
            rspacep = rtemp * rprob
            # print(spacep,bip)
            # print(spacep,rspacep)
            # print(result[t],(spacep+rspacep)/2)
            # 0.05
            if ((prob+rprob)/2) >= 0.25:#(((bigram[bi]*prob)+(rprob*bigram[rbi]))/2):#spacep > bip and rspacep > bip:
                # print(spacep,rspacep,(spacep+rspacep)/2)
                result[t] = result[t] + ' '
                # print(result)
                text = ''.join(result)
                result = list(copy.deepcopy(text))
                # result = list(copy.deepcopy(text))
                temp = prob#bigram[text[t]+' ']
                rtemp = rprob#bigram[' '+text[t+1]]
                
            else:
                temp = prob#bigram[bi]
                if text[t+1]+text[t+2] in bigram:
                    rtemp = rprob#bigram[text[t+1]+text[t+2]]
                else:
                    rtemp = rprob#unigram[text[t+1]] * unigram[text[t+2]]
        else:
            temp = bigram[bi]
            # rtemp = bigram[text[t+1]+text[t+2]]
            if text[t+1]+text[t+2] in bigram:
                rtemp = bigram[text[t+1]+text[t+2]]
            else:
                rtemp = unigram[text[t+1]] * unigram[text[t+2]]
        t += 1
        # print(t,len(text))
        if (t+1) >= (len(text)-1):
            break 
    print(''.join(result))
    # for k,v in bigram.items():
