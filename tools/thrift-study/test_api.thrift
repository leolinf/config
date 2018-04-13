namespace py test


exception TestException {
    1: string           respcd;         //异常码
    2: string           respmsg;         //异常描述信息
}

// 用户状态
enum USER_STATUS {
    NOT_BIND=1,  // 未绑定手机号
    BIND=2,  // 未激活
    ACTIVED=3, // 已绑定手机号并激活
}


enum USER_ROLE {
    OPUSER=1,  // 销售人员
    STORE=2,  // 门店（商户）。交易发生所在，最小的USERID
    STORE_MGR=3,  // 门店管理人员。 可管理多个门店
    DISTRICT=4,  // 大区
    DISTRICT_MGR=5,  // 大区负责人
    PARTNER=6,  // 合作商
    LENDER=7,  // 放款方（资金提供方）
    BORROWER=8,  // 借款人
}

// 销售
struct Opuser {
    1: optional i64 userid;
    2: optional i64 store_uid;        // 所属门店的USERID，创建必传。
    3: optional string idnumber;     // 身份证号码
    4: optional string name;         // 销售姓名
    5: optional USER_STATUS status;
    6: optional i64 cid;
    7: optional string utime;  // 更新时间， 如： 2018-01-30 00:12:33
}

// 查询元数据
struct QueryMeta {
    1: required i64             offset=0;           // 偏移, 默认从 0 开始
    2: required i64             count=100;          // 记录数, 默认 100 条
    3: optional string          orderby;            // 排序方式, 不同的查询支持的字段不同, 详情参照具体接口的注释。
}

// 销售人员查询参数
struct OpuserQueryArg {
    1: required QueryMeta query_meta;                // 查询元数据
    2: optional string s_join_dtm;                   // 最早注册时间. 形如: '2016-01-02 12:22:33'
    3: optional string e_join_dtm;                   // 最晚注册时间. 形如: '2016-01-30 12:22:33'

    4: optional list<i64> store_uids;                // 所属门店的USERID
    5: optional list<i64> userids;                   // USERID
    6: optional list<string> idnumbers;              // 身份证号码
    7: optional string name;                         // 销售姓名
    8: optional list<USER_STATUS> status;            // 用户状态
    9: optional list<i64> cids;                      // customer服务的CID
}

service TestServer {

    // 销售人员
    Opuser opuser_create(1:Opuser info, 2:i64 admin) throws (1:TestException e);
    list<i64> opuser_query(1:OpuserQueryArg q) throws (1:TestException e);
    map<i64, Opuser> opuser_get(1:list<i64> l) throws (1:TestException e);
    void opuser_update(1:map<i64, Opuser> infos, 2:i64 admin) throws (1:TestException e);
}
