
def heimingdan():
   hei_text =open('./hei_text.txt' ,'r' ,encoding='utf8' ,errors='ignore').readlines()
   hei_text=[i.strip() for i in hei_text]

   return hei_text

if __name__ == '__main__':
    a=heimingdan()
    print(a)