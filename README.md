* 深度学习AI服务器：
    * anaconda
    * gunicorn
    * flask
    * tensorflow
    * keras

* 工作流程：
    * 字牌服务器通过内网发起http请求获取决策。

* 请求数据格式：
    {
        card_current: 0,
        cards_info:
        [
            {
            hand_cards:[],
            desk_front_cards:[],     #上家牌信息
            desk_back_cards:[],
            discard_cards:[]
            },
            {
            hand_cards:[],
            desk_front_cards:[],     #当前玩家牌信息   
            desk_back_cards:[],
            discard_cards:[]
            },
            {
            hand_cards:[],
            desk_front_cards:[],     #下家牌信息     
            desk_back_cards:[],
            discard_cards:[]
            }
        ]
    }
    
* 监听
    * IP
        * beta： 192.168.82.102:5000
        * production: 192.168.180.24:5000

* 服务启动
    * beta：
        * source activate tf1.5
        * gunicorn -w 1 -b 192.168.82.102:5000 app:App

    * production:
        * source activate tf1.5_production
        * gunicorn -w 6 -b 192.168.180.24:5000 app:App 