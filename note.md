## q_time_v1

當 q_time 超過的時候，給予一個負的獎勵，並 terminate 掉。

## q_time_v2

以超過多少給予負的獎勵，並 terminate 掉。

## 後續

加入 Q-time remain 的 feature，讓 GNN 有辦法多一個代表 Q-time 緊急程度的特徵去做決策。

效果相對之前的版本還不錯，但整體超過率還是有點高。

後來就是想用 or-tools 對 Q-time ration 做驗證，確認兩倍的 Q-time ratio 是真的很難解，還是模型解很爛。