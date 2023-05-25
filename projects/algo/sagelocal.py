\begin{sagesilent}
def Groverize_complixity(x):
    return  (2 - (1/(x))^2)^0.5

def genrator_running_time():
    d = 4
    c_values = [ 3 , 3.592  , 4     , 1.6181 , 4      , d      , 3.3146 , 2.3146     , 8 , 6 , 4 ,
                 d , 1.9102 , 8     , 1.5538 , 1.2738 , 2.0755 , 3.0755 , (d-0.9245)
                   , 1.2738 , 2.562 , d      , d      , 3.6181 , 2.168  , (d-0.832)]

    i = 0 
    while True:
        yield f"{Groverize_complixity(c_values[i]):.5}^{{k}}"
        i += 1

genr = genrator_running_time()

\end{sagesilent}
