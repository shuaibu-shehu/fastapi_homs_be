-- DropForeignKey
ALTER TABLE "DailyOxygenConsumption" DROP CONSTRAINT "DailyOxygenConsumption_department_id_fkey";

-- AlterTable
ALTER TABLE "DailyOxygenConsumption" ALTER COLUMN "date" SET DEFAULT (CURRENT_DATE);

-- AddForeignKey
ALTER TABLE "DailyOxygenConsumption" ADD CONSTRAINT "DailyOxygenConsumption_department_id_fkey" FOREIGN KEY ("department_id") REFERENCES "Department"("id") ON DELETE CASCADE ON UPDATE CASCADE;
