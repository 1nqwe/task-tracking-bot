import aiosqlite


async def complete_add_task(user_id, task, category=None):
    connect = await aiosqlite.connect('bot\database\db.db')
    cursor = await connect.cursor()
    if None != category:
        await cursor.execute('INSERT INTO tasks (user_id, task, category) VALUES (?, ?, ?)',
                            (user_id, task, category))
    else:
        await cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)',
                             (user_id, task))
    await connect.commit()
    await cursor.close()
    await connect.close()