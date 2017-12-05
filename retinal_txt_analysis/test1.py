'''

task: 多分类问题

1. 在病例文件中，抽取出前5的眼底病
2. 以此5种眼底病作为flag，给每张图片打上标签
3. 将眼底图片按不同眼底病分类到不同的文件夹
4. 查看不同的文件夹。检验是否病例中标为眼病的图片的严重等级都较高；检验是同时归属于不同眼底病的图片；
5. 训练二分类网络，对某一种疾病进行区分，并在kaggle数据集中进行实验
'''

# 1. extract flags from illness case
import pandas as pd

case_file = './caseinfo.csv'
df = pd.DataFrame.from_csv(case_file)
bingli_list = []
img_id_list = []
for index, row in df.iterrows():
    bingli_list.append(row[9])
    img_id_list.append(index)

assert len(bingli_list) == len(img_id_list)

# import jieba
import jieba

total_cnt = len(bingli_list)
empty_cnt = 0
filled_cnt = 0

dict = {}


# 提取指定的眼底病图片所需变量：
case_name = ['青光眼', '白内障', '老年性']
case_list = []
case_img_list = []
for i in range(len(case_name)):
    case_list.append([])
    case_img_list.append([])

for ii, index in enumerate(bingli_list):
    if not isinstance(index, str):
        empty_cnt += 1
        continue
    filled_cnt += 1
    for i,name in enumerate(case_name):
        if name in index:
            case_list[i].append(index)
            case_img_list[i].append(img_id_list[ii])
    res = list(jieba.cut(index))
    for i in res:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1

dict_cut = {}
dict = {key:value for key,value in dict.items() if value > 100}

print(dict)
# 输出结果：{'\\': 1384, 'N': 1089, '右眼': 260, '青光眼': 162, '双眼': 855, '结膜炎': 104, '老年性': 147, '白内障': 271, '左眼': 240, '，': 625, ' ': 601, '/': 118, '晶体': 103, '屈光': 162, '不正': 160, '滴眼': 111}
'''
结果分析：
1. 有效数据太少了。。。太少了。。。我也无力吐槽。。。太少了。。。我想的太天真了。。。无力阿。。。
2. 但即便如此，仍然按照task2记录，提取出前5的眼底标签：青光眼/老年性/白内障。。。是在提不出其他的了，就连这个老年性，我怀疑都是伴着另两种病的；

* 于是，在上述过程中，需要记录，图片编号，以便提取图片
'''

for i, _ in enumerate(case_name):
    print(case_name[i]+':')
    print(case_list[i])

'''
青光眼:
['右眼抗青光眼术后', '青光眼青光眼', '双眼慢性闭角型青光眼\\', '双眼原发性开角型青光眼', '右眼原发性开角型青光眼', '双眼抗青光眼术后\\', '右眼原发性开角型青光眼 右眼小梁术后', '左眼慢性闭角型青光眼 小梁术后', '右眼慢性闭角型青光眼\\', '双眼原发性开角型青光眼\\', '右眼原发性开角型青光眼', '双眼发育性青光眼', '双眼原发性开角型青光眼\\', '可疑性青光眼', '双眼慢性闭角型青光眼\\', '左眼青光眼（闭角型）', '双眼原发性开角型青光眼', '双眼原发性开角型青光眼？', '双眼慢性闭角型青光眼', '双眼原发性开角型青光眼\\', '双眼慢性闭角型青光眼', '左眼慢性闭角型青光眼?\\', '双眼青光眼\\', '双眼急性闭角型青光眼\\', '青光眼临床前期', '左眼急性闭角型青光眼（缓解期），右眼急性闭角型青光眼（临床前期）', '双眼慢性闭角型青光眼', '先天性青光眼', '双眼慢性闭角型青光眼', '双眼原发性开角型青光眼', '可疑性青光眼\\', '双眼抗青光眼手术后 双眼白内障 ', '双眼抗青光眼术后', '左眼急性闭角青光眼\\', '双眼闭角性青光眼临床前期\\', '双眼慢性闭角型青光眼\\', '双眼先天性青光眼', '左眼继发性青光眼？\\', '慢性闭角型青光眼', '急性闭角型青光眼术后', '右眼抗青光眼术后\\', '双眼可疑青光眼', '青年型青光眼', '双眼青光眼', '双眼青光眼 左眼CRVO 双眼NPDR III期', '双眼青光眼', '右眼继发性青光眼', '双眼可疑性青光眼', '双眼可疑性青光眼', '双眼可疑性青光眼', '左眼原发性开角型青光眼', '双先天性青光眼术后', '双眼青光眼术后', '右眼可疑青光眼转诊', '双眼新生血管青光眼', '双眼原发性开角型青光眼，双眼小梁术后', '双眼白内障 双眼可疑青光眼转诊', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；双眼虹膜膨窿/前房浅；  建议：到医院进行排除青光眼检查；', '双眼视网膜动脉硬化；右眼视盘凹陷偏大；  建议：到医院进行排除青光眼检查；', '双眼青光眼？', '双眼开角型青光眼', '双眼慢性闭角型青光眼', '右眼虹膜炎 继发青光眼', '青光眼术后', '右眼黄斑病变 右眼可疑青光眼转诊 左眼高度近视眼底改变', '左眼角膜病变 左眼可疑青光眼转诊', '双眼闭角型青光眼术后', '左眼可疑青光眼', '双眼先天性青光眼\\', '双眼急性闭角型青光眼', '双眼抗青光眼术后 \\', '双眼慢性闭角型青光眼激光虹膜打孔术后\\', '双眼原发性开角型青光眼\\', '左眼抗青光眼术后\\', '左眼青光眼\\', '双眼慢性闭角型青光眼', '左眼绝对期青光眼\\', '绝对期青光眼', '青光眼待排', '慢性闭角型青光眼\\', '右眼新生血管性青光眼\\', '双眼可疑性青光眼', '双眼慢性闭角型青光眼\\', '双眼原发性开角型青光眼？', '右眼急性闭角型青光眼\\', '右眼原发性开角型青光眼', '右眼急性闭角型青光眼', '左眼青光眼', '双眼闭角型青光眼', '左眼急性闭角型青光眼\\', '双眼原发性开角型青光眼\\', '双眼抗青光眼术后\\', '左眼急性闭角型青光眼', '双眼原发性开角型青光眼', '左眼继发性青光眼\\', '慢性闭角型青光眼', '左眼继发性青光眼', '右眼急性闭角型青光眼 左闭角青光眼慢性期\\', '双眼慢性闭角型青光眼', '左眼抗青光眼术后眼压失控\\', '右眼可疑性青光眼\\', '双眼慢性闭角型青光眼\\', '原发性开角型青光眼', '双眼急性闭角型青光眼', '双眼青光眼', '右眼慢性闭角型青光眼\\', '双眼先天性青光眼', '双眼可疑性闭角型青光眼\\', '右眼眼球挫伤 前房积血 继发性青光眼', '双眼先天性青光眼\\', '青光眼', '双眼开角型青光眼', '双眼慢性闭角型青光眼\\', '双眼抗青光眼术后', '右眼原发性开角型青光眼', '双眼慢性闭角型青光眼\\', '双眼原发性开角型青光眼\\', '双眼原发性开角型青光眼', '左眼抗青光眼术后 双眼开角型青光眼 ', '双眼可疑青光眼', '左眼激素性青光眼 左眼炎性假瘤 双眼并发性白内障', '双眼原发性开角型青光眼', '双眼原发性开角型青光眼', '右眼开角型青光眼', '右抗青术后 左慢闭青光眼 双白内障', '双眼激光周边虹膜切开（LPI）术后；双眼慢性闭角型青光眼；左眼小梁切除术后', '双眼青光眼 双眼白内障', '双眼青光眼', '继发性青光眼', '双眼慢性闭角青光眼 白内障', '左眼慢性虹膜炎；左眼继发性青光眼', '左眼慢性闭角型型青光眼；左眼滤过性手术后；左眼恶性青光眼', '右眼青光眼激光术后', '双眼小梁切除术后 残余性青光眼', '右眼急性闭角型青光眼', '双眼急性闭角型青光眼', '原发性开角型青光眼', '青光眼', '双眼原发性开角型青光眼\\', '右眼青光眼激光术后', '正常眼压性青光眼', '正常眼压性青光眼\\', '左眼可疑青光眼', '双眼急性闭角型青光眼\\', '双眼原发性开角型青光眼\\', '双眼先天性青光眼', '右眼原发性开角型青光眼？  黄斑水肿', ' 1: 青光眼白内障', '双眼原发性开角型青光眼青光眼', '左眼急性闭角型青光眼 缓解期？', '双眼原发性开角型青光眼', '继发性青光眼晶状体脱位', '双眼慢性闭角型青光眼 左眼新生血管青光眼\\', '双眼慢性闭角型青光眼', '双眼慢性闭角型青光眼']
白内障:
['右眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障', '左眼白内障手术后', '左虹膜炎\u3000\u3000左玻璃体混浊\u3000\u3000左眼高近\u3000\u3000\u3000右眼黄斑病变\u3000\u3000双白内障\u3000', '结膜炎白内障', '双眼白内障', '左眼白内障（原因待查）', '左眼白内障\\', '双眼老年性白内障\\', '老年性白内障', '白内障\\', '右眼白内障', '双眼老年性白内障初期', '左眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障\\', '双眼老年性白内障', '双眼抗青光眼手术后 双眼白内障 ', '右眼角膜水肿 白内障术后 右眼翼状胬肉 左眼老年性白内障', '左RD 双白内障 左角膜瘢痕', '双眼白内障', '结膜炎白内障', '双眼白内障（右眼》左眼）', '白内障术后\\', '右眼白内障\\', '右眼白内障 左IOL术后', '右眼老年性白内障\\', '双眼老年性白内障中期', '右眼白内障', '双眼白内障，双眼眼底未见明显异常', '双眼老年性白内障初期', '双眼白内障（未熟期）\\', '双眼老年性白内障', '左眼老年性白内障（后囊下性）', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼睑裂斑 双眼老年性白内障 双眼视乳头血管炎 ？ ', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼白内障 双眼黄斑病变(黄斑前膜) 双眼视网膜病变(出血)', '右眼白内障 左眼白内障术转诊', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼白内障术转诊', '双眼白内障', '双眼白内障', '双眼老年性白内障（皮质性），双眼青排', '双眼白内障', '双眼白内障', '右眼人工晶体眼 左眼白内障术转诊', '右眼白内障术转诊 右眼虹膜后粘连', '双眼白内障高度近视眼底改变', '双眼老年性白内障', '老年性白内障', '老年性白内障', '右眼老年性白内障（过熟期）', '双眼老年性白内障', '双眼老年性白内障', '白内障 黄斑变性', '双眼白内障', '右眼白内障 左眼角膜病变', '双眼白内障 双眼可疑青光眼转诊', '右眼白内障 左眼人工晶体眼 双眼黄斑病变', '双眼白内障', '双眼白内障', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；双眼虹膜膨窿/前房浅；  建议：到医院进行排除青光眼检查；', '双眼白内障(晶体轻度混浊)；  建议：定期到医院进行眼科随诊观察；', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；左眼视网膜前膜；黄斑裂孔？；  建议：到医院进一步眼科检查/治疗；', '右眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；左眼晶状体皮质混浊明显；  建议：定期到医院进行眼科随诊观察；', '双眼白内障(晶体明显混浊)；双眼视网膜动脉硬化；  建议：可以考虑白内障手术；', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；右眼豹纹状眼底；左眼豹纹状眼底，可疑视盘下方视网膜出血；  建议：定期到医院进行眼科随诊观察；', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；  建议：定期到医院进行眼科随诊观察；', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；  建议：定期到医院进行眼科随诊观察；', '双眼白内障(晶体轻度混浊)；双眼视网膜动脉硬化；  建议：定期到医院进行眼科随诊观察；', '双眼白内障(晶体明显混浊)；  建议：可以考虑白内障手术；到医院进一步眼科检查/治疗；', '右眼白内障手术后', '右眼白内障手术后', '右眼白内障手术后', '左眼白内障手术后', '右眼白内障手术后 右眼无法判读', '右眼白内障手术后 右眼黄斑病变?', '右眼白内障手术后', '双眼白内障', '双眼白内障 右眼黄斑病变', '右眼白内障术转诊', '双眼白内障术转诊', '双眼老年性白内障', '右眼角膜感染 外伤性白内障术后', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右眼老年性白内障', '双眼老年性白内障', '双眼白内障', '双眼白内障', '双眼白内障 左眼陈旧性视网膜血管病变（视网膜静脉阻塞）', '双眼白内障 右眼翼状胬肉转诊', '双眼白内障', '双眼白内障', '双眼白内障', '双眼老年性白内障', '双眼白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼白内障', '双眼老年性白内障', '双眼双眼老年性白内障', '右眼老年性白内障', '糖尿病 双眼糖网？双眼白内障\\', '双眼白内障', '右眼并发性白内障', '双眼白内障', '双眼白内障\\', '右眼老年性白内障；左眼IOL；双眼脉络膜萎缩', '双眼老年性白内障', '双眼白内障\\', '白内障', '老年性白内障', '双眼白内障术后', '双眼白内障右眼明显', '双眼白内障', '双眼白内障', '双眼白内障\\', '双眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障\\', '双眼白内障', '双眼白内障\\', '双眼先天性白内障', '右眼白内障', '双眼老年性白内障\\', '双眼白内障', '双眼老年性白内障\\', '双眼老年性白内障（未成熟期）\\', '白内障\\', '先天性白内障', '双眼老年性白内障\\', '双眼高度近视眼底 右眼角膜白斑 双眼白内障 双眼干眼 ', '双眼老年性白内障', '双眼糖尿病视网膜病变，右眼VH， 双眼白内障', '右眼高度近视眼底 左眼白内障', '双眼白内障', '双眼白内障', '双眼白内障', '双眼白内障 左眼黄斑病变', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障，眼底？', '右泪囊炎  左人工晶体眼  右白内障', '双眼老年性白内障', '右眼翼状胬肉转诊 右眼白内障 左眼人工晶体眼', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右IOL术后 左眼老年性白内障', '左眼激素性青光眼 左眼炎性假瘤 双眼并发性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右抗青术后 左慢闭青光眼 双白内障', '双眼白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼青光眼 双眼白内障', '双眼老年性白内障    双眼浅前房', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼慢性闭角青光眼 白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '左睑缘炎  干眼症   白内障', '双眼老年性白内障中期', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '左眼角膜裂伤缝合术后 左眼外伤性白内障', '双眼老年性白内障', '双眼老年性白内障初期', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障\\', '双眼白内障\\', '左眼老年性白内障中期', '双眼老年性白内障中期', '双眼老年性白内障中期', '双眼老年性白内障初期', '左眼白内障', '白内障\\', '双眼白内障', '双眼老年性白内障初期', '双眼老年性白内障', '双眼老年性白内障初期', '右白内障', '双眼白内障，双眼底未见明显异常', '双眼白内障，豹纹状眼底', '双眼白内障，双眼底可见处未见明显异常', '左眼糖尿病视网膜病变，双眼白内障', '左眼老年性白内障(未成熟期)\\', '双眼老年性白内障\\', ' 1: 青光眼白内障', '双眼白内障', '双眼白内障术后ＩＯＬ眼', ' 1:白内障 ', ' 1:白内障 ', '双眼白内障（右眼》左眼）', ' 1:白内障  2:干眼症  3:结膜炎 ', '白内障白内障']
老年性:
['右眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障', '双眼老年性白内障\\', '老年性白内障', '双眼老年性白内障初期', '左眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障\\', '双眼老年性白内障', '右眼角膜水肿 白内障术后 右眼翼状胬肉 左眼老年性白内障', '右眼老年性白内障\\', '双眼老年性白内障中期', '双眼老年性白内障初期', '双眼老年性白内障', '左眼老年性白内障（后囊下性）', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼睑裂斑 双眼老年性白内障 双眼视乳头血管炎 ？ ', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障（皮质性），双眼青排', '双眼老年性白内障', '老年性白内障', '老年性白内障', '右眼老年性白内障（过熟期）', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼双眼老年性白内障', '右眼老年性白内障', '右眼老年性白内障；左眼IOL；双眼脉络膜萎缩', '双眼老年性白内障', '老年性白内障', '双眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障\\', '双眼老年性白内障（未成熟期）\\', '双眼老年性白内障\\', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障，眼底？', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '右IOL术后 左眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障    双眼浅前房', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障中期', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障初期', '双眼老年性白内障', '双眼老年性白内障', '双眼老年性白内障\\', '左眼老年性白内障中期', '双眼老年性白内障中期', '双眼老年性白内障中期', '双眼老年性白内障初期', '双眼老年性白内障初期', '双眼老年性白内障', '双眼老年性白内障初期', '左眼老年性白内障(未成熟期)\\', '双眼老年性白内障\\']


其中，老年性的标签里基本都是陪着老年性白内障的，因此，真正需要提取的标签就青光眼和白内障
'''

for i, _ in enumerate(case_img_list):
    print(case_name[i]+':')
    print(case_img_list[i])


'''
extract image:
'''
import os
import shutil
from glob import glob
extract_root = './extracted'
os.makedirs(extract_root, exist_ok=True)
extract_path_list = []
for i, name in enumerate(case_name):
    tmp = os.path.join(extract_root, name)
    os.makedirs(tmp, exist_ok=True)
    extract_path_list.append(tmp)
print('extracted path:')
print(extract_path_list)

raw_root = '/media/weidong/weidong/1w图片/baidutupian'
raw_img_list = glob(os.path.join(raw_root, '*.jpg'))
raw_img_head_list = [os.path.basename(i).split('.')[0].split('--')[0] for i in raw_img_list]
raw_img_head_dict = {value:key for key,value in enumerate(raw_img_head_list)}
case_img_raw_list = []
for i in range(len(case_name)):
    case_img_raw_list.append([])
for i in range(len(case_name)):
    tmp = case_img_list[i]
    for j, img_file in enumerate(tmp):
        if img_file in raw_img_head_dict:
            i_raw = raw_img_head_dict[img_file]
            case_img_raw_list[i].append(raw_img_list[i_raw])

for i in range(len(extract_path_list)):
    tmp_root = extract_path_list[i]
    for j in case_img_raw_list[i]:
        basename = os.path.basename(j)
        dstname = os.path.join(tmp_root, basename)
        shutil.copy(j, dstname)
        print('copy from {} to {}'.format(j, dstname))


'''
看了整理出来的图片，我的疑问就是：是不是图片和病例的编号，对应给错了，举例：编号为1307680的图片和病例
'''