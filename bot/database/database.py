import aiosqlite


async def add_user(user_id, full_name, username):
    connect = await aiosqlite.connect('bot/database/db.db')
    cursor = await connect.cursor()
    check_user = await cursor.execute("SELECT * FROM users WHERE (user_id) = ?", (user_id,))
    check_user = await check_user.fetchone()
    if check_user is None:
        await cursor.execute("INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)",
                             (user_id, full_name, username))
        await connect.commit()
    await cursor.close()
    await connect.close()

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

async def count_user_tasks(user_id):
    async with aiosqlite.connect('bot/database/db.db') as db:
        async with db.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?",
                              (user_id,) ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

