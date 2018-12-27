/*
thrift接口定义文件
*/

namespace py hello

exception FenqiException {
	1: string respcd;
	2: string respmsg;
}
enum STATUS {
	SUCCESS=1,
	FAIL=2,
}

const i16 test=123;

struct Msg{
	1: optional string name;
}

service HelloService {
    string say(1:Msg info);
	void test(1:i64 test_info) throws (1: FenqiException e);
}
