from ipywidgets import widgets,interactive
import numpy as np
from time import time, sleep
from datetime import datetime
from os.path import abspath,exists
from os import mkdir

def run_fips_tests(v_bits):
    len_v_bits=v_bits.shape[0]
    nb_nibble=int((v_bits.shape[0])/4)
    v_nibble=np.zeros((nb_nibble,),dtype=np.uint8)
    for i in range(4):
        v_nibble+=np.array(v_bits[i:4*nb_nibble:4],dtype=np.uint8)*(2**i)

    T1=v_bits.sum()

    T2=0
    for j in range(16):
        fj=(v_nibble==j).sum()
        T2+=((fj-5000.0/16)**2)/(5000.0/16)

    nb_lambda=32
    m_T3=np.zeros((nb_lambda,2),dtype=np.float64)
    for lambda_i in range(nb_lambda):
        word_size_in_bits=lambda_i+3

        nb_words=int(len_v_bits-word_size_in_bits)
        v_words=np.zeros((nb_words,),dtype=np.uint64)
        for i in range(word_size_in_bits):
            v_words+=np.array(v_bits[i:i+nb_words],dtype=np.uint8)*(2**i)    

        patern_0=2**(word_size_in_bits-1)+1
        patern_1=(2**(word_size_in_bits)-2**(word_size_in_bits-1)-2)
        m_T3[lambda_i,0]=(v_words==patern_0).sum()
        m_T3[lambda_i,1]=(v_words==patern_1).sum()

    v_cnt=np.zeros((2,),dtype=np.uint64)
    cnt_tmp=0
    for i in range(len_v_bits-1):
        if v_bits[i]==v_bits[i+1]:
            cnt_tmp+=1
            if v_cnt[int(v_bits[i+1])]<cnt_tmp:
                v_cnt[int(v_bits[i+1])]=cnt_tmp
        else:
            cnt_tmp=1
                
    v_T4=v_cnt
    
    v_T5=np.zeros((5000,),dtype=np.uint64)
    for tau in range(5000):
        v_T5[tau]=(v_bits[:5000]^v_bits[tau+1:tau+5000+1]).sum()
    return (T1,T2,[[m_T3[0,0],m_T3[0,1]],[m_T3[1,0],m_T3[1,1]],[m_T3[2,0],m_T3[2,1]],[m_T3[3,0],m_T3[3,1]],[m_T3[4,0],m_T3[4,1]],[m_T3[5:,0].sum(),m_T3[5:,1].sum()]],v_T4,v_T5)


image_value_relativ_sigma=	b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00-\x00\x00\x00%\x08\x06\x00\x00\x00\xd6I`\xf7\x00\x00\x03\xf8IDATx^\x95\x98\x8du\x157\x14\x84M\x07\xd0B\xd2A\xd2B\xd2\x01\xb4\x00\x1d@\x0bI\x07I\x0bI\x07\xd0B\xd2\x01i!t\x00\xe8[\xfc\xe9\xcc\x8e\xef>\x9bsf\xfc\xa4\xb9?\xbaO+i\xe5wwww\xe0Y\x11L\xda\x84\x17\x8bo\x16\xffX\xfc\xb8\xf8\xff\xe2\x97\xe2\xe7ASO\x9b\xfd\xd6\xc8\xf9\xcf\xe2\xab\xc5]\xcbT\xe0\xa4%^.\x92\xe8\xd6\x80ikM=m\xf6\xaf\xb4O\x8b\xbb\x96.p\x1b\x06\xfc\xb4\xf8\xdf\xe2S\x06I\xad\xed\xf6Sk\xbd\xc9\xb8\xbb\xb6.x\x1b\n\xbf-f\xe2i\xb0+\xad\xed\xf6Sk\xbd\xf9nq\xd7v\xabP\xf4\x1f\x17\xff]\xec$=\x08\x8f\xcfu\x9d\xb6\xabbX^M\xc6I\xa2\xfd\xb5\xc8r<\xd5y\xabh\n\xa6\x98iP\x8a\xf9s\xf1\xd7\xc5)\x07\x1b\xe7\xc3\xe2U\xd1,\xb5\x86y\xa6|[KC;\xfe\xb0\x98\x053\xb8\x05\xf8\xa8:\xa6\xdb\xf0\xf5\xa2\xb1I\xbe\xd0U\xac0G\xf2\xdb\x9f{lq\x81\x82\xfb\xf8b \x1e?\xb3\xafo\xc6\x80n\xdb\x7f\xbb\xd8E\x93\xf3\xe7E\x91\xb1\xc2\x1c\xc9s\'@q&\xb6`\xd6X\xfb\x89\xcc1\xe5\xa3\xef\xa9\x93dy\t\xe3\x92#&\x07\x16~\xce\x06dC\xdcJ\x94\xb6\xc9\x8f>/\xa1,\x18\xf2E\x84q\xc9\x11m`\x97\x92\xac\x8bf\xb9\x88L\xd8\xc9\xedO\x1a\xcb*\xf3\xda~\xbe(:\x16\xa8m[:\x10\xec:\xce\xe4\xccPb\x07W\x1b\xd8\xbf\xd22\xaf\xed<E:\x16d\xfc\xb6\xd9\xe1\xfe\x90I\xe1\xe9-t\x8fS\xf0=\xd4Z\x07i3o\x92\xa7\x0b2V\xffno p\xf1\xb1\xe0,\x9aY\xee\x80)\x89Z\xeb mY\xac\xe4H\x04\x19\xab\x7f\xb7\x0f\xd8\xc9Y\xb6h\xceha\xe0)8\x90\xf6[~=)\xd0\x99\x06Sl\xe6<l\xfca-g\xc1&\xe5\x05"NA\x03\xd2~\xe5\xc7f\xce\xfc\xf2\xbb\xd74\x7f<\x8a:!\xbb=\xb1\x83\xee\xd1\xed\xc9n\x9fO^$\xe6v,\xe8\xcb*al\xeb\x07\x10y\x9dv\xd1O\xd9\x80\xdd\x9e\xec\xf6\xf9\xe4\xc9MEw\x1cPk}\xc3D\x99\xf0\xf7\xc5\x0cL\x8an\xdb\x9f\xfc\xe0\xdf\x8b9\x06\xe4\x88m\x7f\xa0\x96\xfa\xee\xfb2I\x92,onM\xd1m\xfb\x93\x1f\x9c._\xbc}\xdb\x1f\xa8\xa5\xbe\xfb^\xec\x9bO\xc1\x94\x18\xa4\xae\x8du\x9b\xc5Z<\xd7\xd7\t\x19\x9b\xb9\x0e\xad\x8f:\xc8e\xe9)8%\n\xa4\xae\xcd\xf5\xec\x18\x16\xdd\xb1"cmo\xcdM\x98d\xed\xb5cRd{B\xfa{\xc3\xcb\xa2\xdf/\x02\xfd2_\xf7O\x98\xae\x8b}\xc1o\x8alO\xd0\x9f\xf3\xd9\xdcY\xf4/\x8b@\xbf\xcc\xd7\xfd\x13\xb8rvB_\xab \x83\xa7D\xad\xd9O\x8d}\xd3c0\xcb\xe9\xdb1\xd9O\xfb\xa1\x11\xdc\t\x9d\x01\xb0\x1d\xab-Z\xb3\xaf\xe6\xdb\xb6\xc7`\xf6\xd37c@\xf6\xd3~hlD\x13\xca\xc7\x8aN6\xdaf~\x8b\xa5}\xb5g@\xb6E\xfa\x1c\xb6\xe9\x9c\xbe\xba\xc0d`\xea\x89\xb4y\xd7 \xa7E\xb3\x87\xb8Q\xa6\x9f\x04\xd9\x16\xe9s\xd8\xf2\xb2d\xd1\xd3E)\x91\t&\xbb\xc8\x93\xc91\xa6{\x86\xb8\xca7i\xc7\xba\xce\xa2\x19L\xdcJ\x92l\xf0\xdf\xb7\xf9,\x9a\'x\xe5\x0f\xae\xf2=\xd0\xe8\xb0\x86\x9d\t\x8b\xf7\x11\n\x03\x9b\x13x\xcbu\xc1|\x89\xc4\x94c\xd2\xc0\x03\xcd\x8e\xb3m\xd1\x9e\xd5\xc2\xc0f\xe3\xb1="\xa6\x1c\x93\x06\x1eh\n\xcc\xac\xbf\xc1\xc9<\x96\x12jI\xd0\'\x05\x17$\x7f\x8c\x99\xfcEjmo\xdf\x03:A\x8a\xcc\xc2i3h\x07f\x0c\xc4\x87\x97\x141\x16\xcd\x93\xcbM\xd71\x89\xd4\xda\xde\xbe\x07\xda\x81\x818\x96,\x9c"\xb8[\xa3\'8uX\xbb\xfc\xea\x94\xb3\xcbe\xcbk\xad\xe8\xb6\x14\x93&F[v\xd2\x81W\xb9\xbf\x81H\xfa\xfe\\\xe6\x17\x92\xccl\xfeW\xddy\x85\xb6\xc741\xda\xb2390k\xfc\xde\xc6\x8c\xbat\xf8d9\xf0fc\xc3\xb2\x1f\x12\x9d\xa3\xdb\x93\xbd5\xf1\xc0\xf6\x15\xadS\xe4>\x16\xc5\x0cP\x00\x00\x00\x0ctEXtlatex\x00\\sigma~\x00\xc2B\x00\x00\x00\x0etEXtresolution\x00600\xf2~\xdd&\x00\x00\x00\x0ctEXtcolor\x00000000\xc2\x9f\xf6\xa1\x00\x00\x00\x16tEXtSoftware\x00latex2png.comJ\x05\xa9\n\x00\x00\x00\x00IEND\xaeB`\x82'
image_value_M=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00E\x00\x00\x00&\x08\x06\x00\x00\x00\x92\xedV\xdd\x00\x00\x05\xa5IDATx^\x9d\x9a\r\xb1$E\x10\x84\xdf9\x00\x0b\xe0\x00,\x80\x03\xb0\x00\x0e\xc0\x028\x00\x0b\xe0\x00,\x80\x03\xb0\x00\x0e\xe0\xfa\xdb\xb8o#\xb7.\xbbg\xdfEd\xc6\xedTwe\xff\xd7T\xcf\xbb\x97\x97\x97-\xbeZ\xfcs\xf1\xdfw\xe4\xf7\xcf\x8b\x9f.\xbey\xc7\x06\xcb\xe4\xc7\x8bh\xfd\xb4\xf8\xc7"Z\xff/\xfe\xb7\xf8\xd7\xe2/\x8b\xdf.N=\xfd\xaf\x80/\xfd\xfa{Q\xed\x7f\x16\xd5\xfef\xf1\xa3E\xf5v\x9aW\xe5\xb7\x01\xd0i\x1apR\xf8-\x7f\\\xbc\x12g2\xe8,\xf5\xd1\x92<3\x80i\x83\xdf-\x8aS\x07\x19d\xf61I_S[~\xbfx\xd2\xb4\xec\xa1\\\x83\x03\xa1\xe3\x9f-\x8a\x1f\x16\xb3\x11VA\xa4 \xa4\x03hP\x8fUc\x00jY\x07\xb0\x83\xa8\x93\x83\xfa}1\xb5\x92\x80\x95O\x1f\xb5s7\xb0 _/\xa6.>\xbf-&R;y\x07\x0f\n1\xdb\x08O0@\xc4%\x1d\x04)\xc8\xa0\xecH\xae\xbc\xb0\x9e`@\xd6\x97,LjJw\x07t\xe5\x13\xb3\xfe\xe7\x8bj\xea\x87\x86\x98\xf5\xe5\xc3\x03\xbb\x03\x01Vp\x82\xf2\x1c\xb0\xbc\x89,\xb0R\xc4\x0c\x1a\xe6\xdfO\x16S[\x8a\xb4\xb1\xeb\xec\xb44v\tV\x99\xf6\x88m\x94\x89\xd4\x11i\xc3\x0f\xbd\xec\xf3\xdc\xb5\x93\xf7\x1f\xee\x12\x1am\xa0\x8eG+I\xa0\x03NHnQ\xb5\x93"m\x1e\xa3\xa4\xbb\x058\xb0<Z\xc2\xe7\x9d\xad\x1dQwK\xd6K\xde\xc1d\xe4 \x1bX\xd1\x14\xa71\x1ap\xa5\xe7\x99\x15\xb5\xc1\x80\xdb\x1c\r\xc9\x11\xa6\xbe\x0b\xc1\x844\xa4\xb6L\xe4\x11\x92j\xef|n`\xab\xebP+\xbc\x03\xbb!\xc5s\x10\x94\xedpl|\x81\xf85\xf5xf\x81\xf8\x97c\xbd\xf3Mm\x99\xe0\xa8\xd9\xdf$m\xee|n\x06\xdf\x163\xf2O\x10hS8\x070c@"5eb\xd7q\x88>\x8b\x06\xaetD\x96\xe3k\x1f\xa7f\xd6{\x00\x86<:\xbb\x8a\x04\xd2&\x0e\x89G\xcdG\xa4f\xab\xf7\xe5b\xea&[\xee\xb2\xd3\x11Y\xfe\xc5\xe2\xab\'\x05\xe84W;\x9dZ\xc0\x82Lh\xd6kl\xc8rs\x8fI\xb2\xd2\xd7\xa0\xb5\xe7\x11L]\x9e[\xcaq\x873\x99\xc1G\xf8\x0c\xcd\x11rB \x81,\xeb56dy\xe6\x1f\xc9\x96\x1a\x9c\xd0\xda3P\xa7\xaec\xdd\x82\x94\x1d\xa7Lj\x84\x8d@V-\x85\xa1\xc15\xeb}\x08\xd5\xce\xc9&~\x81\xac\xf7,\xd2\xa7i\xb7\x97B\xfa\xdc\xce3\x01\xd6`\x96\xb0\x12[-\'C\x92\xfa\x83\x14|-S;;\xder\x89gq\xa5m\xbf\x13\xb5\x9d4N\x12H\x9b8\x13\xda\xea\xcbg\xe0\xf1\x9d\xda\x19\xbc\x1bE\xb3\x89L\nS\x9b6\'\xaaN\x1a\'9\x97M\xbc\xd5M>\x83\xbch\xa6\xf6\xcc#&E\xb3\x89\x8cU\xa9\xddPu\xd289\xaf\xfa\xf0\x94\xacM4M\x81\x8e\x9av\x9a@(\x9a\x0fH\xfb\x8e\xe8\xa8i\x1bd\xdd\x96\'\xd2\xef\x8e4&Y\xb1\x14\x95\xed\\\xee\xd0tEj:\x80_\x17E\xf3\x01io\x9c\t\xa1m\x90\xf7X\'\x91\xbew\xa41\xe9E1;\x0f\xdb\xb9\xdc\xa1\xe9\x82\x8c\'\xd0\x01\xe4\xfdk\xfa\x88\xb47\x9a\xa5K\xdb\xe0\x86l\x9dD\xfa\xd6\n\x89\x99C\xd8\xc8\xc9\xe7\x04\xdb\x83\xb3\xe3\x92U\x16Y\xbf1\x91\xb6\xf9*\xe6\xb7\xc9`\xf3}\xc0U\x85\x99\x9f\xd0\x80Y\xec\x87\xc0\xf6`\xfb>3\x13\xab\xac\xdf\x98\xd0\xe6}\xc7\xfeB~\xcf\x14b\x0b+$\x85\xf1d\xd2o\xb4\x8d\x89S9\xbf\xa7.\x1d\xcf\xcf\x9c`\xfa\xcb\x06\xcb\x88\x1bN\x8aD\xff\x94}?\xe0T\xc1x2y\xcaO\x12\xa7\xf2\xf6\x9d\x83\xce\xfb\x89S4\r\xd8`Y\xbe\xd1\xa4\x9f\x1fv|@3jkw\x12:?}|\xde1\xa1\xad\xad&\x9c\x99\xf5\x95\xce,\xcf\xa3\x03\x9d\xf0\xb6\xbb\x13\x0f\xf6S\x856\xe3y+\x16>\xef\x98\xd0\xe6\'\xc6\xa4\xf7\x9d\xc4\x95\xce,\xcfd\x10:)~\x01\x98\xf5\x05\xbb\x9fT\x80\x90q\xc7t\xd8\xc5\x93\xa7\xef\r\x81,\x97M{\xc6\x93\x89\xa6\x93\xe0\x99@\x9d\x93\x02yY\xec|\x84/\x14?j\xdf\x90Np\xf7\xe1\xe7\xe9{C \xcba\x8b\'p\xc6\x93\x89\xa9\x03\x13\xf6yNJ&l\xd3\x07\xe4\x91\xbb!+\'\xfd\xa4 u\xe2\x0b\xdc\tMkb\x17O\xae\xb6x\xb3\xa7\xad\xfd\xb5\x01>\x1c\x89\x80~\x8e\x95\xe3\xc3\xf3\xbd`\xd2O\x94\x92N\x9b\xfc\x9c\xd0\xb4&v\xf1\xe4\xca\xb7\xd9\xd3\x96w\x1d\xe9w\xe7\x06\xfd\xfc{\x97o\xd5-\xe8h\x8a\xf3\xcc\xdbH\xa1tN[\xb2\x01{\xea\xaaM<\x99\xfe\x93\'\xb4\x84\r\xb6\xbfb&=r-\xc8?\xc0;I\x8a\xf3\xcc\xf7\x89\x14\x14iK6\x9c\xf2\x93\xa6\x91<!\xefQ\xa9\xedqoz\xd0\x13\xf1\x10\xcfZE\xcf\x98\x8d\xc8\x19O\x9a\xef\x15v\xd9f\x8b\'\'\xbdY\xde&\xc5+\xc3NG\x9f\xf7v\x89NIg\xcfF`\x8b\'\xcd\xf7\n-\x9ed\xe7\'w\x98\xe5\xbcJ\xd5sRZN\x95\xf05\xfc\xde\x07r\x9d\x92\x8a\'\xfd\xdbn\xe3k\xd0\x82\xa1\xf9I\xd3L[cbj\xe7w\x99\t\xe2#u\xe6\x1f\x00o\x9a\xd3\xc0\x99o\x93r\xfaf\xfa,\x08\x86\xd9i\xd9\x82\xa1H[c\xc2\xbf\xf1H\x06\xdc`\xd6\xcb[\x87\xd7\xf5I\xf3\x06:\xe8Dd\x03:7L\xd1\x1dw\x17\xccS\xee\xd3t\x92\x13\\MR;\xff\xdb\x05\x0b\xee\xe7\n&$\xdb=i\xd6\x80\x95\x97\xa9\x86\x14<\xb1\xbdy8\x96\'4\x9d\xe4\x04\x03\xe5\xd8\xa8\xcf8\x88\x1d\xd9\xe6{w\x9c\x85\x93\xe6\rl/"2gt\xde.\x1b\xb2\xfc\x8a|mC\x17\x1a\xa7N\x98\xfe\x93\r\xd8\xc9?\xd8\x15\x8c\x83\x89\xa1=&\xc3\x04m\xfaj{\xf3\x16\xdf~\xd6G]t\xf9\xc0\x00\x00\x00\x07tEXtlatex\x00mZ\x8a\xbf \x00\x00\x00\x0etEXtresolution\x00600\xf2~\xdd&\x00\x00\x00\x0ctEXtcolor\x00000000\xc2\x9f\xf6\xa1\x00\x00\x00\x16tEXtSoftware\x00latex2png.comJ\x05\xa9\n\x00\x00\x00\x00IEND\xaeB`\x82'
image_value_D=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x009\x08\x06\x00\x00\x00\x86D-\xd7\x00\x00\x06\xc5IDATx^\x9d\x9a\x81\x91\xe54\x10D\x97\x0c \x05\xc8\x00R\x80\x0c \x05\xc8\x00R\x80\x0c \x05\xc8\x00R\xb8\xcb\x00R\x80\x0c\xe0\xd4\xbf\xb6\xcds\xbb%\xebo\xd5\xeb\xaa\xf5\xcchF\xd6\xb7,[\xde\x97\x97\x97\x97\x8f^\xd5\xb0\xaf\xc5\xfc>\xf4\xef\xd0\x7f\xaf\xd2\xdfV\xb3=#\xb7\xa7\xe8\xffs\xe8\xdd\xd0oC\xbf\x0c}9d\xb2\xcf\x949\xd9\xd2I\x18\xc8\x98\x8f\x87\xb2\xb3\xec`\xb3=#\xb7\xa7Vq>\xfeu\xe8\xab\xa1\xec\xb7eN\xb6t\x12\x06f\xcc\xb7C?\x0f\xe9\x17\x90T\\W\xc5\xdfC\xabN[\x8aU\xfb&\xe7\xa4\x9c_\xbf\xbes\xb4::~?\xf4\xc5\xd0\xac\xff\'\xdb\xd2\xb9\x80q\x19\xabKs6\x00\x1a ]A\xd9\x9e9vl\xba\xec5X\x99\x9f\x83"\x7f\xe3\x94\x8bI\xc5\xc9\xb9\x80q\x19\xfb\xc3\xd0l\x00\xbe\x1f\x12\xd9\x9e9vmF9\x9d\x9f\x03 \xe9^\x91\x9cre\xd2\x93s\x01\xe32vu\x05|:$\xb2=s\xec\xda\x88\xf2\xeads\x00$\xd9u\xd5\x99S\xaeUR\x06fL\xb3\x99\x7f\x86\xdc\x11Jv\xe6\xcb\x1c\xcf\xfa,\xf2\xc7\x10kr\x10\xcc\xa9mKb\x18\x981\xcd&\xf4K\xb0\x03\x94\xae\x0c\xe6\xcb\x1c\xcf\xfa,\xa2c\xdd\x04]\x93W\xc2\x8fC\xe2\xd4\xf6\xf8\xa3\xc0\xc0\x8ci6\xa1\xd5\x81\'M}7\xc4|\x99\xe3Y\x9fEt\xfc\xc9\x90kr\x00$\xdd<Omy0\x93\xd9\xf1y\xfegq\x1d\x7f6\xc4\xb6;Z\xb1\x8a\xd1\xaf\xed\xba\xd4_C\'Xl&\xb3\xe3\xe3\xfc\xe7\x00\xcc\xe6\xff\x9dV\xacbt\xd3\xe33\t\xf5\xf5\xd0\x01\x8b\xcdd\xee|\xfa\x85Y\x88\x030\x9b\xffwZq\x17\xa3\xe7\x00\xf6\xc7jK\xe32\xd9\xaeO\xf3_\'\xebB\x1c\x00\xf9\x84\xe3)\x93\xc73\xd8v\xa5o\x86\xd8\x07K}\xf3\x93\xe2\x81\x1b5v}z\\u\x81\x1c\x80g\xd6\xff;\xd8v%\xdd\x0c\xd9\x07K}\xfbiH1\x07n\xd4\xd8\xf5i\xce\xb9\x00\x07@v\xe3x\xca\xe4\xf1\x0c\xb6\xbd\x13\xdf\x1d,\xf5MK\xa5\xfc\x07n@lk\xbe\x84\xf3\x9f\x85$\xcd\xff\x1dZ\x1d\xd6o~\xb1\xf2i\xbeg\x7f||\xa2%`\xe2\xf4%Z\xe3\xb3\x80\x8f\xe5\xdb\xa1\xd5a\xfd\xe6\x17+\x9f\xa7%\xfb\xe3c\xee#\xd4\x04L\x9c\xbe\xa4\xad\xff>\xd6\xd5\xb1C\xab\xc3\xfa\xcd/V>\xbe1f\xff|c~\xd0\x120q\xfa\x92\xb6\xfe\xebo\xaf\xff;\xb4:\xb6Q\xc9\xca\xb7\x1a\x80\xc7\x9bi6l\xc9\xf2X0N\xbf\xb0\x93f!]\x82\x82\xf1\x12I\x1b\xe3\xd2\'\x9a-q\xccj\x00\x1e\xef\x06\x99\xcc\xc7\xcdF\x18\xa79\xee\xa4Yh\xb6\xfe\x93\xb41.}\xa2\xd9\x12\xc7x\xef2\xfb%=6L2\x99\x8f\x9b\x8d0N\xf3\xdfI\xb3\xd0\xe7C\x82\xf1\x12I\x1b\xe3\xd2\'\x9a-q\xccj\x15\xf0\xd5y\xc2\r\x9b\x08m^\xffS|\xfeOl\xa7\x8f\xb6\x14i\xfe\x94\x99\xdd\x9b$\xed5^h\xc9,b\x9b\x9e\xf0x\xd2\x946\'Z[a;}\xb4\xa5H\xf3\xa7\x8cO\xb6\r\x80\x9e\x06/\xb4d\x16\xb1\xcd\xcf\xffM\xda\x1blm\x85\xed\xf4\xd1\x96"\xcd\x9f\x12\x9a~\xab\x01P\xff.\xcc\x92\xcd\xd0e\xc4"\x92\x0by\xfe\x8bU\xae\x9d:\x8e\xd9\x8d\x13z\xedm\xfd\xf2\xb1^\x96.\xb0\x10\x93\xcd\xd0\x06\x03\x8bH.DV\xb9v\xea8f7N\xe4\xebp\x0e@}@c!&kh\xd3\x81\x05,\x15\xd1\xf2CV\xb9\xee\xea\x08\xc7\xec\xc6\t\xad\x00\xd9/\x0e\xc0)\x97\x1b6\x99\xb4\xeb\x12b\x01KE\xbc\xffo\xdc\xc60\xcf\xca\xf7V\xd4\xd6}\xc9\x13\x97\xa6o\x83M&\xedm\xfeK*\xc6\xf9/\xdc\xc60\xcf\xca\xf7V\xb4\xe1\xe1\xbe\xb4\x01\x98\xee\x074\x99\xb4\xb7\xf9/\xa9X\xe26\x86yV\xbe\xb7\xa2\x13t_\xda\x00\x1c;B;\x85Z\x8c\xbf\x10;!\x0bq\xfdom\xc5\xae\xaf\xc54\x7f\xca\x1b!<i\xf7\xef\xf4\x80v\xfc\xb1\xa0\xc5h\x89a\x01\'\x97\xb8\xfe\xb7\xb6b\xd7\xd7b\x9a\x9f\xe2VX\x1b\x00M]\xc7\xfe\xff\xc7\x82\x16\xe3\xb7\xac6\x00\xabO\xd3f\xd7\xd7b\x9a\x9f\xe2\xcbY\x1b\x00\xf6\xef\x02\x13%\xf4\xe5%\xe6\xe4Rk\xcf\xb63_\x83m2n\xe6\xcb\xe5\x8f}\xac[\xe2$\x93\x11\xdb\xdb%\xe6c\xad\xff\xad\xbdm+_\x83m2\xae\xf9\xfcn\xc2\x13g\x1fO\x1fE\x1aL\x96\xd8\xce\xfdv&\x97\xb4\xfe\xb7\xf6\xb6\xad|\r\xb6\xc9\xb8\xe6\x9b}\x12\x93t\xd5\xde\xc2d\x89\xed\xba\x89\xcc\x06@\xeb\x7fko\xdb\xca\xd7`\x9b\x8ck\xbe\xdc\x9a\xa7n\x7f}\xd1\x92\xa6\xb8\xfe\xe7@\xc8o\xb2\xdd\xae\xee\x98\xc5\xe9\xcd\xd4\xfdH\xf9\xc9\xef6\xbf\x83f\xe2\xa7g\x89\x03\xe0\xf5\xdfd\xdb]\xdd1\x8b\x9b}\x0c\x95\x96w~\xe2\xa0\x99\xf2\xf9\x9f\x03\xe0\xf5\xdfd\xdb]\xdd\xd1\xe2\xbc/\xc1\xbeY\\\xf7/\xf9\xd3\xc8\xc0\x94\xe0.k\x16<\x1e/_\xc9\xb6\xa4\xf9Z,\xe3Rd\xf6Y\x8e\xcb^kw1\xfa\xb8I\xe4\xb76\x0e\x00\xe3D\xb6%\xcd\xd7b\x19\x972\xb3\xado\rJ\xfb\xe7\xa8\x13i\xf4q\x93\x9f\xff)\x17l\xfb\x7fl\x9b4_\x8be\\J\xe8\xf3V\xeb\x8f\xfe>}\xfa\x1a\xb0\xdd\x01\x13^\x9c\x81\x9f\xff\x9b\xf8\xfe\x9f9[\xde\xe6\x9b\xc5\x8a\x16/tE\xfa\xa4\xa9\xdc\x8f\x10\xccq\xe4\xba\x18\x16\xe4\xfc\xa7\xda\xfe\xdf*o\xf3\xcdbE\x8b\xcf\xffG\xb0f_\xa3\x99\xe3\xc8u1,\xc8\xf9O\x91\xcc\xd9\xf26\xdf,Vd\xbc\x9f\xf8\xa4<\xf9\x9d\x1c\xd6\xc1\xc50``\xfe\xb7\x05\x8bj\xfe\x13\xb6\x9b\x89\xa4\x8dqMm\xb3C\xd2\x15\x9a\xb1$}\'\xff\xc50``\xfe\xbf\r\x07 \xf7\xd7\xd9n&\x926\xc6\xa5\xdagx\xc9s>\xe3I\xfaN\xfe\x8ba\xc0@>\xffK\x1c\x00\xfd\x8f>a\xbb\x99H\xda\x18gi\x0b\x9b\xff\x01*\xb9/\xfc\xce\x9f\xedH\xfaN\xfe\xa5s\xb0;\xff\xdfB\xd6\xcb>\xe43\xbe\xebj\x9d\xbf[\xea2\x97h\xb6\x931\x9d\xab\xef\x7f\xb7\x1b\x0c\x1bd=\x1f\xeb\xcaR~\xd5\xc9\x01\xd0\xbe\x03\x1fr\xcc,\xd7\x9d\xeddL\'\xef\xb8\xa9\xb6\xde>K\xd6\xd3\xfdF7V\xfe\xda>ymh\xae^k3\x97\x8f\xefl\x07tJ|\xf9\xe1\x89\xdb&\x7fM4\xc8\\\xb38\xcdo\xe5\xd1}\x86\x9f\xb3\xb3\xe6\xecFG\x99<\x16\xcd\xf6\xb8\x8c4\xc7\xf4+k\x19Q\'t\xa7\xd5/\xb0\xea\x8cm\x8aQ\xbc\xda*\x07\xa5\xe5*\xa58=\xc0\xe8\x12\xd6\xe5\xbdz\x85\x95t\xef\xc9\xab\xcc\'\xd2d\xf2X4\xdb\xe5\xe9\xaeu\xc2Z\xc5\xd17\x8b\xd9\x8d\xd3\xa0\xea\x87\xc8\xd5\xc5\xf8D\x9aL\x1e\x8bf{\x8c\xee\xaa3\xd4*\x8e\xbeYL\xc6\xe9\xd7\xd7/\xac\xe5M\'\xac\xed\xec\xdcRo\xd0\x9f2y,.\xb6\x0fV\xd8\x96\xd3\xd8-\x91\xec\x00\x00\x00\x07tEXtlatex\x00D\x188\'L\x00\x00\x00\x0etEXtresolution\x00600\xf2~\xdd&\x00\x00\x00\x0ctEXtcolor\x00000000\xc2\x9f\xf6\xa1\x00\x00\x00\x16tEXtSoftware\x00latex2png.comJ\x05\xa9\n\x00\x00\x00\x00IEND\xaeB`\x82'


image_height=350
image_width=150
param_height=15
cell_height=30
cell_width=70
cell_width_col0=130
cell_width_col1=100
cell_width_collast=150
cell_width_title=cell_width_col0+cell_width_col1+cell_width_collast+cell_width*2

mean_delay=3.125e-10 
log10_jitter_min=-4
log10_jitter_max=-2
nb_log10_jitter=int(1E5)
v_log10_jitter=log10_jitter_min+(log10_jitter_max-log10_jitter_min)*np.arange(nb_log10_jitter,dtype=np.float64)/(nb_log10_jitter-1)
v_jitter=10**(v_log10_jitter)
v_jitter[0]=0

log10_ratio_period_sample_min=2
log10_ratio_period_sample_max=6

nb_log10_ratio_period_sample=int(10**(log10_ratio_period_sample_max)-10**(log10_ratio_period_sample_min))

v_log10_ratio_period_sample=log10_ratio_period_sample_min+(log10_ratio_period_sample_max-log10_ratio_period_sample_min)*np.arange(nb_log10_ratio_period_sample,dtype=np.float64)/(nb_log10_ratio_period_sample-1)
v_ratio_period_sample=np.array((10**(v_log10_ratio_period_sample))*np.pi*0.5,dtype=np.uint64)
p_opt=5
nb_bits=20000
nb_nibble=int((nb_bits)/4)

v_std_dev_value_widgets_option=[]
for i in range(v_jitter.shape[0]):
    v_std_dev_value_widgets_option.append('%.2e'%(v_jitter[i]))
    
box_layout = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%cell_width,border='1px solid gray',margin='0px 0px 0px 0px',justify_content='center',align_items='center')
box_layout2 = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%(2*cell_width),border='1px solid gray',margin='0px 0px 0px 0px',justify_content='center',align_items='center')
box_layout_col0 = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%(cell_width_col0),border='1px solid gray',margin='0px 0px 0px 0px',justify_content='center',align_items='center')
box_layout_col1 = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%(cell_width_col1),border='1px solid gray',margin='0px 0px 0px 0px',justify_content='center',align_items='center')
box_layout_collast = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%(cell_width_collast),border='1px solid gray',margin='0px 0px 0px 0px',justify_content='center',align_items='center')
box_layout_title = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%(cell_width_title),border='1px solid gray',margin='0px 0px 0px 0px',justify_content='center',align_items='center')
box_layout_down = widgets.Layout(height='%dpx'%cell_height,width='%dpx'%(cell_width_title),margin='0px 0px 0px 0px',justify_content='center',align_items='center')



v_items=[]

v_items_h=[]
v_items_h.append(widgets.HTML(value='<p align="center"><b>Procedure A of AIS31</b></p>',layout=box_layout_title))
v_items.append(v_items_h)

v_items_h=[]
v_items_h.append(widgets.HTML(value='<p align="center">Statistical Test</p>',layout=box_layout_col0))
v_items_h.append(widgets.HTML('<p align="center">Test Result</p>',layout=box_layout_col1))
v_items_h.append(widgets.HTML('<p align="center">Test value</p>',layout=box_layout2))
v_items_h.append(widgets.HTML('<p align="center">Valid range</p>',layout=box_layout_collast))
v_items.append(v_items_h)

v_items_h=[]
v_items_h.append(widgets.HTML('<p align="center">Monobit test</p>',layout=box_layout_col0))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout_col1))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout2))
v_items_h.append(widgets.HTML('<p align="center">[9655 ; 10345]</p>',layout=box_layout_collast))
v_items.append(v_items_h)

v_items_h=[]
v_items_h.append(widgets.HTML('<p align="center">Poker test</p>',layout=box_layout_col0))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout_col1))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout2))
v_items_h.append(widgets.HTML('<p align="center">[1.03 ; 57.4]</p>',layout=box_layout_collast))
v_items.append(v_items_h)

m_T3_bounds=[[2267,2733],[1079,1421],[502,748],[223,402],[90,223],[90,223]]
for i in range(6):
    v_items_h=[]
    if i==5:
        v_items_h.append(widgets.HTML('<p align="center">Run test &#x3BB &ge; %d</p>'%(i+1),layout=box_layout_col0))
    else:
        v_items_h.append(widgets.HTML('<p align="center">Run test &#x3BB=%d</p>'%(i+1),layout=box_layout_col0))
    v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout_col1))
    v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout))
    v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout))
    v_items_h.append(widgets.HTML('<p align="center">[%d ; %d]</p>'%(m_T3_bounds[i][0],m_T3_bounds[i][1]),layout=box_layout_collast))
    v_items.append(v_items_h)

v_items_h=[]
v_items_h.append(widgets.HTML('<p align="center">Long Run test</p>',layout=box_layout_col0))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout_col1))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout2))
v_items_h.append(widgets.HTML('<p align="center">[0 ; 33]</p>',layout=box_layout_collast))
v_items.append(v_items_h)


v_items_h=[]
v_items_h.append(widgets.HTML('<p align="center">Autocorrelations test</p>',layout=box_layout_col0))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout_col1))
v_items_h.append(widgets.HTML('<p align="center"> </p>',layout=box_layout2))
v_items_h.append(widgets.HTML('<p align="center">[2326 ; 2674] </p>',layout=box_layout_collast))
v_items.append(v_items_h)

nb_lines=len(v_items)
v_hb=[]
for i in range(nb_lines):
    v_tmp=v_items[i]
    nb_row=len(v_tmp)
    v_box=[]
    for j in range(nb_row):
        v_box.append(v_tmp[j])
    v_hb.append(widgets.HBox(v_box))
v_box_table=widgets.VBox(v_hb)

std_dev_value_widgets=widgets.SelectionSlider(options=v_std_dev_value_widgets_option,layout=widgets.Layout(height='%dpx'%(2*param_height),width='%dpx'%(2*image_width)))
std_dev_value_widgets_png_desc=widgets.Image(value=image_value_relativ_sigma,format='png',layout=widgets.Layout(height='%dpx'%(param_height)))    

sample_period_value_widgets=widgets.SelectionSlider(options=list(v_ratio_period_sample),layout=widgets.Layout(height='%dpx'%(2*param_height),width='%dpx'%(2*image_width)))
sample_period_value_widgets_png_desc=widgets.Image(value=image_value_D,format='png',layout=widgets.Layout(height='%dpx'%(param_height)))    

m_value_widgets=widgets.IntSlider(value=1,min=1,max=16,step=1,layout=widgets.Layout(height='%dpx'%(2*param_height),width='%dpx'%(2*image_width)),readout_format='d')
m_value_widgets_png_desc=widgets.Image(value=image_value_M,format='png',layout=widgets.Layout(height='%dpx'%(param_height)))    

raw_bytes=widgets.Textarea(value='',rows=5000,placeholder='',description='',disabled=True,layout=widgets.Layout(height='%dpx'%(image_height),width='%dpx'%(0.5*image_width)))

progressbar_widgets=widgets.IntProgress(value=0,min=0,max=nb_bits,description='',bar_style='',style={'bar_color': 'maroon'},orientation='horizontal',layout=widgets.Layout(height='%dpx'%(2*param_height),width='%dpx'%(2*image_width)))

html_download=widgets.HTML(value='',layout=widgets.Layout(width='%dpx'%(6*image_width)))
save_data_in_file_widgets=widgets.Checkbox(value=False,description='SAVE RANDOM NUMBERS IN A TEXT FILE',disabled=False,button_style='', tooltip='Description',icon='check',layout=widgets.Layout(width='%dpx'%(2*image_width)),style={'description_width': 'initial'})

v_list_nb_premiers=[5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,199]


if not('T0' in locals()):
    T0=3*mean_delay*2

if not('v_T' in locals()):
    v_T=np.array(v_list_nb_premiers)*mean_delay*2

"""    
print('T0=%e sec.'%T0)
for i in range(m_value_widgets.max):
    print('T%d=%e sec.'%(i+1,v_T[i]))
"""    

def generate_rnd(std_dev_value_widgets_in,sample_period_value,m_value,save_data_in_file):
    
    std_dev_value=v_jitter[v_std_dev_value_widgets_option.index(std_dev_value_widgets_in)]
    duty_cycle_value=0.5


    T_sampling=sample_period_value*T0    
    
    raw_bytes.value=''
    m_raw_bits=np.zeros((nb_bits,m_value),dtype=np.uint8)
    
    for m_index in range(m_value):
        half_period=0.5*v_T[m_index]


        M=((T_sampling)/half_period)
        M-=p_opt*np.sqrt(M)*std_dev_value
        if M>=0:
            M=int(M)
        else:
            M=0
        half_M=int(M/2)

        #ros_state=(np.random.rand())<duty_cycle_value
        ros_state=0
        m_raw_bits[0,m_index]=ros_state
        tmp_half_per=half_period*2*abs(ros_state-duty_cycle_value)
        #current_phase=np.random.rand()*tmp_half_per
        current_phase=0
        progressbar_widgets.value=0
        t0=time()
        for i in range(1,nb_bits):

            tmp_half_per=half_period*2*abs(0-duty_cycle_value)
            current_phase+=half_M*tmp_half_per+std_dev_value*tmp_half_per*np.sqrt(half_M)*np.random.randn()

            tmp_half_per=half_period*2*abs(1-duty_cycle_value)
            current_phase+=half_M*tmp_half_per+std_dev_value*tmp_half_per*np.sqrt(half_M)*np.random.randn()

            while (current_phase<=(i*T_sampling)):
                ros_state^=1
                tmp_half_per=half_period*2*abs(ros_state-duty_cycle_value)
                current_phase+=tmp_half_per+tmp_half_per*std_dev_value*np.random.randn()
            m_raw_bits[i,m_index]=ros_state^1
            if (time()-t0)>0.01:
                progressbar_widgets.value=int(m_index*(nb_bits/m_value)+(i/m_value))
                t0=time()
            
    v_raw_bits=np.array((m_raw_bits.sum(1))%2,dtype=np.uint8)
    
    v_nibble=np.zeros((nb_nibble,),dtype=np.uint8)
    for i in range(4):
        v_nibble+=np.array(v_raw_bits[i:4*nb_nibble:4],dtype=np.uint8)*(2**i)

    (T1_o,T2_o,M_T3_o,v_T4_o,v_T5_o)=run_fips_tests(v_raw_bits)
    v_items[2][2].value='<p align="center">%d</p>'%T1_o
    if abs(T1_o-nb_bits/2)<346:
        v_items[2][1].value='<p align="center"; style="color:#00FF00";> PASS </p>'
    else:
        v_items[2][1].value='<p align="center"; style="color:#FF0000";> FAIL </p>'    
    
    v_items[3][2].value='<p align="center">%.2f</p>'%T2_o
    if (T2_o<57.4)&(T2_o>1.03):
        v_items[3][1].value='<p align="center"; style="color:#00FF00";> PASS </p>'
    else:
        v_items[3][1].value='<p align="center"; style="color:#FF0000";> FAIL </p>'    

    for i in range(6):
        cnt_error=0
        for b in range(2):
            v_items[4+i][2+b].value='<p align="center">%d</p>'%M_T3_o[i][b]
            if (M_T3_o[i][b]<m_T3_bounds[i][1])&(M_T3_o[i][b]>m_T3_bounds[i][0]):
                cnt_error+=1                
        if (cnt_error>0):
            v_items[4+i][1].value='<p align="center"; style="color:#00FF00";> PASS </p>'
        else:
            v_items[4+i][1].value='<p align="center"; style="color:#FF0000";> FAIL </p>'
    
    longest_run=v_T4_o.max()
    v_items[10][2].value='<p align="center">Longest run : %d</p>'%(longest_run)
    if (longest_run<34):
        v_items[10][1].value='<p align="center"; style="color:#00FF00";> PASS </p>'
    else:
        v_items[10][1].value='<p align="center"; style="color:#FF0000";> FAIL </p>'   

    max_autocor=v_T5_o.max()
    min_autocor=v_T5_o.min()
    v_items[11][2].value='<p align="center">MIN=%d MAX=%d</p>'%(min_autocor,max_autocor)
    if (max_autocor<2674)&(max_autocor>2326)&(min_autocor<2674)&(min_autocor>2326):
        v_items[11][1].value='<p align="center"; style="color:#00FF00";> PASS </p>'
    else:
        v_items[11][1].value='<p align="center"; style="color:#FF0000";> FAIL </p>'  
            
    s_line_raw_bytes_value=''
    for i in range(nb_nibble):
        s_line_raw_bytes_value='%s%X'%(s_line_raw_bytes_value,v_nibble[i])
    raw_bytes.value=s_line_raw_bytes_value   
    
    
    if save_data_in_file==True:
        now = datetime.now()
        str_time = now.strftime("%d-%m-%Y_%Hh%Mm%Ss%fms")
        randomvalues_file_name='ex1_a%s_jit%s_D%d_%s.txt'%(duty_cycle_value,std_dev_value,sample_period_value,str_time)
        if exists('random_values')==False:
            mkdir('random_values')
            
        fid_rnd_file=open('random_values/%s'%randomvalues_file_name,'w')
        fid_rnd_file.write(s_line_raw_bytes_value)
        fid_rnd_file.close()

        path_to_download='%s'%(randomvalues_file_name)
        s_line_for_download='<p> random numbers are saved in the following file %s stored in %s</p>'%(path_to_download,abspath('random_values'))
        html_download.value=s_line_for_download
    else:
        s_line_for_download=''
        html_download.value=s_line_for_download

interactive_plot = interactive(generate_rnd,{'manual': True}, std_dev_value_widgets_in =std_dev_value_widgets ,sample_period_value=sample_period_value_widgets ,m_value=m_value_widgets,save_data_in_file=save_data_in_file_widgets)
interactive_plot.children[-2].description='GENERATE RANDOM NUMBERS'
for i in range(3):
    interactive_plot.children[i].description=''
interactive_plot.children[-2].layout=widgets.Layout(width='%dpx'%(2*image_width))  
v_box_top=widgets.VBox([widgets.HBox([widgets.VBox([interactive_plot.children[-2],widgets.HBox([m_value_widgets_png_desc,m_value_widgets]),widgets.HBox([std_dev_value_widgets_png_desc,std_dev_value_widgets]),widgets.HBox([sample_period_value_widgets_png_desc,sample_period_value_widgets]),progressbar_widgets,save_data_in_file_widgets]),raw_bytes,v_box_table]),html_download])
#display(v_box_top)    
