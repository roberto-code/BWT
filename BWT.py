	
class BWT:

    def __init__(self, saBucketSize, freqBucketSize, refStr):
        self.endCode = ord('$')
        self.minCode = ord('a')
        self.maxCode = ord('z')

        self.saBucketSize = saBucketSize
        self.freqBucketSize = freqBucketSize

        self.rank = self.count(refStr)
        print self.rank

        sa = self.sfxArray(refStr)
        self.bwt = self.BWTransform(refStr, sa)

        self.saCache = [ sa[i*saBucketSize] for i in range( int( ( len(sa)-1 )/self.saBucketSize ) ) ]

        freq = {cc:0 for cc in range(self.endCode,self.maxCode+1)}

        self.freqCache = dict()
        for i in range( len(self.bwt)+1 ):
            if i % freqBucketSize == 0:
                bucket = int(i/self.freqBucketSize) #int not really necessary since i % freqBucketSize == 0
                self.freqCache[bucket] = freq.copy()
            if i < len(self.bwt):
                freq[ ord(self.bwt[i]) ] += 1


    def sfxArray(self, refStr):
	    a = list(range(len(refStr)+1))
	    return sorted(a, key=lambda x:refStr[x:])


    def BWTransform(self, refStr, sfxArray):
        bwt = ''
        for pos in sfxArray:
            bwt += '$' if pos == 0 else refStr[pos-1]
        print(bwt)
        return bwt

    def recover(self):
	    pos = 0
	    ans = '$'
	    for i in range( 1,len(self.bwt) ):
		    ans = self.bwt[pos] + ans
		    print("ans",ans)
		    pos = self.inverse(pos)
	    return ans     

    def inverse(self, pos):
	    ch = self.bwt[pos]
	    chCode = ord(ch)
	    return self.rank[chCode] + self.occ(ch, pos)  
        
    def count(self, in_str):
        freq = dict()
        for i in range(self.endCode,self.maxCode+1):
            freq[i] = 0

        freq[self.endCode] = 1
        for i in range( len(in_str) ):
            bcc = ord( in_str[i] )
            if bcc not in freq:
                print("Error!!")
            freq[bcc] += 1
		
        c = dict()
        c[self.endCode] = 0
        for i in range(self.endCode+1, self.maxCode+1):
            c[i] = c[i-1] + freq[i-1]

        return c

    def multiplicity(self, pattern):
        low = 0
        high = len(self.bwt)
        for c in pattern[::-1]: #reverse
            if high <= low:
                break
            low = self.rank[ord(c)] + self.occ(c, low)
            high = self.rank[ord(c)] + self.occ(c, high)
        return high - low

    def locations(self, pattern):
        low = 0
        high = len(self.bwt)
        for c in pattern[::-1]:
            if high <= low:
                break
            low = self.rank[ord(c)] + self.occ(c,low)
            high = self.rank[ord(c)] + self.occ(c, high)
        for i in range(low,high):
            print( "Pattern {} is located at {}".format( pattern, self.locate(i) ) )
        return		

    def locate(self, pos):
        count = 0
        while pos % self.saBucketSize > 0:
            count += 1
            pos = self.inverse(pos)
        return (count + self.saCache[ pos // self.saBucketSize ]) % len(self.bwt)

    def occ(self, ch, loc):
        if loc < 0:
            return 0

        bucket = int(loc/self.freqBucketSize)
        lo = bucket * self.freqBucketSize
        count = self.freqCache[bucket][ord(ch)]
        for j in range(lo,loc):
            if self.bwt[j] == ch:
                count += 1
        return count

    def approx(self, pattern, errsLeft):
        self.approxB( pattern, errsLeft, len(pattern)-1, 0, len(self.bwt) )

    def approxB(self, pattern, errsLeft, loc, lo, hi):
        if errsLeft < 0:
            return
        if loc < 0:
            for i in range(lo,hi):
                print( "Approximate pattern found at {}".format( self.locate(i) ) )
            return

        self.approxB(pattern, errsLeft-1, loc-1, lo, hi)
        patLoc = ord(pattern[loc])
        for sy in range(self.minCode, self.maxCode+1):
            rankSy = self.rank[sy]
            syAsChar = chr(sy)
            lo2 = rankSy + self.occ(syAsChar,lo)
            hi2 = rankSy + self.occ(syAsChar,hi)
            if lo2 < hi2:
                self.approxB(pattern, errsLeft-1, loc, lo2, hi2)
                e2 = errsLeft
                if sy != patLoc:
                    e2 -= 1
                self.approxB(pattern, e2, loc-1, lo2, hi2)

        return



if __name__ == "__main__":

    myString = "atcgatgatacagactacgaact".lower()
    print(myString)
    xx = BWT(4,5,myString)

    yy = xx.recover()
    print(yy)

    multi = xx.multiplicity("gataca")
    print(multi)

    xx.locations("gataca")

    xx.approx("gataca",1)


