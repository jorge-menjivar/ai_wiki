# from typing import Optional
# from psycopg import sql, AsyncConnection
# from psycopg.rows import TupleRow


# async def get(
#     aconn: AsyncConnection,
#     title: str,
#     commit: bool = False
# ):

#     # Get the section content for a specific title
#     acur = await aconn.execute(sql.SQL(
#         '''
#         SELECT *
#         FROM tasks.ai_content
#         WHERE title = {title}
#         '''
#     ).format(title=title))

#     fetch: Optional[TupleRow] = await acur.fetchone()

#     if commit:
#         await aconn.commit()

#     return fetch


# async def add(
#     aconn: AsyncConnection,
#     title: str,
#     commit: bool = False
# ):

#     # Add the content to a new section in the database
#     await aconn.execute(sql.SQL(
#         '''
#         INSERT INTO tasks.ai_content (title, timestamp)
#         VALUES ({title}, NOW())
#         '''
#     ).format(title=title))

#     if commit:
#         await aconn.commit()


# async def delete(
#     aconn: AsyncConnection,
#     title: str,
#     commit: bool = False
# ):

#     # Get the section content for a specific title
#     await aconn.execute(sql.SQL(
#         '''
#         DELETE FROM tasks.ai_content
#         WHERE title = {title}
#         '''
#     ).format(title=title))

#     if commit:
#         await aconn.commit()
