PROG	START	0		
		LDA		X1
		ADD		X2
		STA		R
HALT	J		HALT

X1		WORD	5
X2		WORD	7	
R 		RESW	1