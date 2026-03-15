insert into User(email,password,first_name,last_name,administrator_flg,update_user_id,update_at,update_number,del_flg)
values
('user01@gmail.com','user01','Duy','Hoan',True,1,datetime('now'),1,False),
('user02@gmail.com','user02','牧島','もえ',True,1,datetime('now'),1,False),
('user03@gmail.com','user03','富士フィルム','XT30II',True,1,datetime('now'),1,False);


insert into Channel(channel_name,overview,user_id,update_at,update_number)
values 
('Java基礎','Javaについてのナレッジを共有します',1,datetime('now'),1),
('SpringFramework','SpringFrameworkについてのナレッジを共有します	',1,datetime('now'),1),
('Jenkins','Jenkinsについてのナレッジを共有します',1,datetime('now'),1),
('Git','構成管理ツールのデファクトスタンダードになりつつあるGitを学ぼう。aaa',1,datetime('now'),1),
('Python','Pythonプログラミングについてのナレッジを共有します',1,datetime('now'),1),
('JavaScript','JavaScriptプログラミングについてナレッジを共有します',1,datetime('now'),1);
 
insert into Knowledge(knowledge,channel_id,user_id,update_at,update_number)
values
('Javaを取得できれば、Webサービスだけではなく組み込み系やデスクトップアプリなど',1,1,datetime('now'),1),
('Javaは「プラットフォムに依存しないプログラミング言語である」',1,1,datetime('now'),1),
('テスト',1,1,datetime('now'),1),
('テスト',1,1,datetime('now'),1),
('Pythonを取得できれば、Webサービスだけではなく組み込み系やデスクトップアプリなど',5,1,datetime('now'),1),
('Pythonは「プラットフォムに依存しないプログラミング言語である」',5,1,datetime('now'),1),
('テスト',5,1,datetime('now'),1),
('テスト',5,1,datetime('now'),1);