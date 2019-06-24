import bisect
def update_cover(coverlist,index1,index2):
    dup_part=[]
    if index1==None or index2==None:
        return (coverlist,dup_part) 
    if coverlist:
        i1=bisect.bisect_left(coverlist,index1)
        i2=bisect.bisect_right(coverlist,index2)
        if i1%2:
            if i2%2:
                dup_part=[index1]+coverlist[i1:i2]+[index2]
                coverlist[i1:i2]=[]
            else:
                dup_part=[index1]+coverlist[i1:i2]
                coverlist[i1:i2]=[index2]
        else:
            if i2%2:
                dup_part=coverlist[i1:i2]+[index2]
                coverlist[i1:i2]=[index1]
            else:
                dup_part=coverlist[i1:i2]
                coverlist[i1:i2]=[index1,index2]
    else:
        coverlist=[index1,index2]
    return (coverlist,dup_part)
    
def maximumPeople(p, x, y, r):
    # first step: obtain cities covered by more than one cloud
    xp=[(x[i], p[i]) for i in range(len(p))]
    xp.sort(key=lambda x: x[0])
    x=[item[0] for item in xp]
    yr=[(y[i]-r[i],y[i]+r[i]) for i in range(len(y))]
    yr.sort(key=lambda x: x[0])
    n=len(y)
    cover=[[]]*n
    for i in range(n):
        xmin,xmax=yr[i]
        index1=bisect.bisect_left(x,xmin)
        index2=bisect.bisect_right(x,xmax)-1
        if index1<=index2:
            cover[i]=[index1,index2]
        else:
            cover[i]=[None,None]
    dup_cover=[] #[dup_cover[2*i], dup_cover[2*i+1]] is the cover range
    single_cover=[]
    for index1, index2 in cover:
        single_cover,dup_part=update_cover(single_cover,index1,index2)
        m=len(dup_part)//2
        for i in range(m):
            dup_cover,_=update_cover(dup_cover,dup_part[2*i],dup_part[2*i+1])
    
    uncovered_count=sum(p)
    m=len(single_cover)//2
    for i in range(m):
        for j in range(single_cover[2*i],single_cover[2*i+1]+1):
            uncovered_count-=xp[j][1]
        
    m=len(dup_cover)//2
    for i in range(m-1,-1,-1):
        xp[dup_cover[2*i]:dup_cover[2*i+1]+1]=[]
    x=[item[0] for item in xp]
    p=[item[1] for item in xp]
    maxm=0
    for i in range(n):
        xmin,xmax=yr[i]
        index1=bisect.bisect_left(x,xmin)
        index2=bisect.bisect_right(x,xmax)-1
        if index1<=index2:
            maxm=max(maxm,sum(p[index1:index2+1]))
    return maxm+uncovered_count
    
p=[10,1,8,3]
x=[4,5,7,2]
y=[3,9,3,5]
r=[11,10,8,7]
ans=maximumPeople(p, x, y, r)