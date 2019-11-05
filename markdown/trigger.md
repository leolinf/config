```sql

use test
delimiter $

create trigger test after insert on test for each row
begin
    insert into test_2(name, sex) values (
        new.name, new.sex);
end
$
delimiter ;
