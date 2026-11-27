import re,collections,time
from google_play_scraper import reviews, Sort, search
for q in []:
    try: print(q,'->',[(a['appId'],a['title']) for a in search(q,lang='vi',country='vn',n_hits=3)])
    except Exception as e: print(q,'search ERR',e)
apps={'ShopeeFood':'com.deliverynow','Grab':'com.grabtaxi.passenger','be':'xyz.be.customer','Shopee':'com.shopee.vn','XanhSM':'com.gsm.customer'}
food=re.compile(r'đồ ăn|do an|món|quán|food|đơn hàng|don hang',re.I)
issue=re.compile(r'thiếu|thieu|sai món|giao nhầm|nhầm món|trễ|tre |chậm|cham|hoàn tiền|hoan tien|hoàn lại|khiếu nại|khieu nai|đổ|nguội|hủy đơn|huỷ đơn|bồi thường|hỗ trợ|ho tro|chăm sóc',re.I)
for name,pid in apps.items():
    t=time.time()
    try: rs,_=reviews(pid,lang='vi',country='vn',sort=Sort.NEWEST,count=10000)
    except Exception as e: print(name,'ERR',e); continue
    ds=[r['at'] for r in rs]
    f=[r for r in rs if food.search(r['content'] or '')]
    fi=[r for r in f if issue.search(r['content'] or '')]
    print(f"{name}: {len(rs)} review ({min(ds).date()}→{max(ds).date()}, {time.time()-t:.0f}s) · nhắc đồ ăn/đơn {len(f)} · đồ ăn+sự cố {len(fi)} · trong đó ≤2★ {sum(r['score']<=2 for r in fi)}")
    for r in fi[:2]: print('   ',r['score'],'★',(r['content'] or '')[:120].replace('\n',' '))
