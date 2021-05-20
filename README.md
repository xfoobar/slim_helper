# slimhelper
Simple helpers

DbHelper:
```
constructor:
    config : Database connection params
    db_type(str): Database type
usage:
    # SQlite:
    from slim_helper.db_helper import DbHelper
    config = {dbname:':memory:'}
    with DbHelper(config,'sqlite') as db:
        db.execute("""
        CREATE TABLE foo (
        id INTEGER PRIMARY KEY ,
        txt TEXT
        )
        """)
        db.execute("insert into foo values(?,?)",[1,'a'])
        db.execute("insert into foo values(?,?)",[2,'b'])
        db.execute("insert into foo values(?,?)",[3,'c'])
        db.commit()
        result = db.query("select * from foo where id=? and txt=?", [2, 'b'])
        print(result)
    # Or
    db=DbHelper(config,'sqlite')
    db.open()
    ...
    db.close()
    
    
    # PostgreSQL:
    config={'host':'localhost','port':'5432','dbname':'foobar','user':'foobar','password':'foobar'}
    with DbHelper(config,'postgresql') as db:
        db.execute("""
        CREATE TABLE foo (
        id INTEGER PRIMARY KEY ,
        txt TEXT
        )
        """)
        db.execute("insert into foo values(%s,%s)",[1,'a'])
        db.execute("insert into foo values(%s,%s)",[2,'b'])
        db.execute("insert into foo values(%s,%s)",[3,'c'])
        db.commit()
        result = db.query("select * from foo where id=%s and txt=%s", [2, 'b'])
        print(result)
    # Or
    db=DbHelper(config,'postgresql')
    db.open()
    ...
    db.close()
```

ParallelHelper:
```
multiprocessing.Pool helper
constructor:
    task (Task): Task object.
    arguments (Iterable[Iterable]):arguments list.
    parallel (int): parallel
usage:
    from slim_helper.parallel_helper import Pool, Task
    def test(a: int, b: str):
        print(a, b)
        return str(a)+b
    p1 = (1, 'a')
    p2 = (2, 'b')
    p3 = (3, 'c')
    task = Task(test)
    params = (p1, p2, p3, p1, p2, p3)
    pool = Pool(task, params, 2)
    r = pool.start()
    print(r)
```