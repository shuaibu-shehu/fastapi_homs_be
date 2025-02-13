-- AlterTable
ALTER TABLE "Bed" ADD COLUMN     "oxygen_consumption" DOUBLE PRECISION DEFAULT 0;

-- AlterTable
ALTER TABLE "DailyOxygenConsumption" ALTER COLUMN "total_consumption" DROP NOT NULL,
ALTER COLUMN "total_consumption" SET DEFAULT 0;
