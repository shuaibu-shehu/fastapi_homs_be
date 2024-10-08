from prisma import Prisma


class PrismaConnection:
    def __init__(self):
        self.prisma = Prisma()

    async def connect(self):
        print('Connecting to Prisma')
        await self.prisma.connect()

    async def disconnect(self):
        await self.prisma.disconnect()


db = PrismaConnection()