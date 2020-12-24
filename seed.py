from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name="Boby", last_name='Brown', image_url='https://images.unsplash.com/photo-1582266255765-fa5cf1a1d501?ixlib=rb-1.2.1&ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&auto=format&fit=crop&w=1350&q=80')
u2 = User(first_name="Mily", last_name='Brown', image_url='https://images.unsplash.com/photo-1438761681033-6461ffad8d80?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NHx8cGVvcGxlfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60')
u3 = User(first_name="Mily", last_name='Brown', image_url='https://images.unsplash.com/photo-1533227268428-f9ed0900fb3b?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlb3BsZXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60')

p1 = Post(title="TheStuff", content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl eros, 
pulvinar facilisis justo mollis, auctor consequat urna. Morbi a bibendum metus. 
Donec scelerisque sollicitudin enim eu venenatis. Duis tincidunt laoreet ex, 
in pretium orci vestibulum eget.""",post_id=1)
p2 = Post(title="MyBad", content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit.""",post_id=1)
p3 = Post(title="Myami", content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl eros, 
pulvinar facilisis justo mollis, auctor consequat urna. Morbi a bibendum metus. 
Donec scelerisque sollicitudin enim eu venenatis.""", post_id=2)
p4 = Post(title="Miao", content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl eros, 
pulvinar facilisis justo mollis, auctor consequat urna. Morbi a bibendum metus. 
Donec scelerisque sollicitudin enim eu venenatis. Duis tincidunt laoreet ex, 
in pretium orci vestibulum eget.""",post_id=3)
p5 = Post(title="Bao", content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit.""",post_id=1)
p6 = Post(title="ZingZing", content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl eros, 
pulvinar facilisis justo mollis, auctor consequat urna. Morbi a bibendum metus. 
Donec scelerisque sollicitudin enim eu venenatis.""", post_id=3)


db.session.add_all([u1,u2,u3])

db.session.commit()

db.session.add_all([p1,p2,p3,p4,p5,p6])

db.session.commit()