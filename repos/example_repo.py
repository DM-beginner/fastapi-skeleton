from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_example(db: AsyncSession):
    stmt = text(
        """
        SELECT id,:column
        FROM example 
    """
    )

    # 2. 执行 SQL，通过第二个参数传递字典进行参数绑定
    # 这种方式会自动处理转义，完美防御 SQL 注入
    result = await db.execute(stmt, {"column": "description"})

    # 3. 获取结果的最佳姿势
    # result.all() 返回的是 Tuple，不方便前端使用
    # result.mappings() 将结果转换为类似字典的对象 (key-value)
    data = result.mappings().all()

    return data
