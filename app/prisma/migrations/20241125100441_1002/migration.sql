-- AlterTable
ALTER TABLE "DailyOxygenConsumption" ADD COLUMN     "patients_count" INTEGER NOT NULL DEFAULT 0,
ALTER COLUMN "date" SET DEFAULT (CURRENT_DATE);
