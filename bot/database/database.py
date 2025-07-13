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
    connect = await aiosqlite.connect('bot/database/db.db')
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

async def get_all_user_tasks(user_id):
    async with aiosqlite.connect('bot/database/db.db') as db:
        async with db.execute(
            "SELECT id, task FROM tasks WHERE user_id = ?",
            (user_id,)
        ) as cursor:
            return await cursor.fetchall()

async def get_task_info(task_id):
    async with aiosqlite.connect('bot/database/db.db') as db:
        async with db.execute("SELECT task, category, is_done FROM tasks WHERE id = ?",
                              (task_id, )) as cursor:
            return await cursor.fetchone()

async def set_is_done(done, task_id):
    async with aiosqlite.connect('bot/database/db.db') as db:
        async with db.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (done, task_id)) as cursor:
            await db.commit()
            return await cursor.fetchone()

async def get_is_done(task_id):
    async with aiosqlite.connect('bot/database/db.db') as db:
        async with db.execute('SELECT is_done FROM tasks WHERE id = ?', (task_id, )) as cursor:
            await db.commit()
            result = await cursor.fetchone()
            return result[0] if result else None


async def delete_task(task_id):
    connect = await aiosqlite.connect('bot/database/db.db')
    cursor = await connect.cursor()
    await cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await connect.commit()
    await cursor.close()
    await connect.close()



async def get_user_count():
    connect = await aiosqlite.connect('bot/database/db.db')
    cursor = await connect.cursor()
    user_count = await cursor.execute('SELECT COUNT(*) FROM users')
    user_count = await user_count.fetchone()
    await cursor.close()
    await connect.close()
    return user_count[0]


async def get_all_users_id():
    connect = await aiosqlite.connect('bot/database/db.db')
    cursor = await connect.cursor()
    all_ids = await cursor.execute('SELECT user_id FROM users')
    all_ids = await all_ids.fetchall()
    await cursor.close()
    await connect.close()
    return all_ids