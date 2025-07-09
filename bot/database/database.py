import aiosqlite


async def complete_add_task(user_id, task, category):
    connect = await aiosqlite.connect('bot\database\db.db')
    cursor = await connect.cursor()
    await cursor.execute('INSERT INTO tasks (user_id, task, category) VALUES (?, ?, ?)',
                         (user_id, task, category))
    await connect.commit()
    await cursor.close()
    await connect.close()