-- AlterTable
ALTER TABLE "DailyOxygenConsumption" ALTER COLUMN "date" SET DEFAULT (CURRENT_DATE);

-- AlterTable
ALTER TABLE "IndividualOxygenConsumption" ADD COLUMN     "daily_oxygen_consumption_id" TEXT;

-- AddForeignKey
ALTER TABLE "IndividualOxygenConsumption" ADD CONSTRAINT "IndividualOxygenConsumption_daily_oxygen_consumption_id_fkey" FOREIGN KEY ("daily_oxygen_consumption_id") REFERENCES "DailyOxygenConsumption"("id") ON DELETE SET NULL ON UPDATE CASCADE;
