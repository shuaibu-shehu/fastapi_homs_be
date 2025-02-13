/*
  Warnings:

  - You are about to drop the column `department_id` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `last_updated` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `patients_count` on the `DailyOxygenConsumption` table. All the data in the column will be lost.

*/
-- DropForeignKey
ALTER TABLE "DailyOxygenConsumption" DROP CONSTRAINT "DailyOxygenConsumption_bed_id_fkey";

-- AlterTable
ALTER TABLE "DailyOxygenConsumption" DROP COLUMN "department_id",
DROP COLUMN "last_updated",
DROP COLUMN "patients_count",
ALTER COLUMN "date" SET DEFAULT CURRENT_TIMESTAMP,
ALTER COLUMN "total_consumption" DROP DEFAULT;

-- AddForeignKey
ALTER TABLE "DailyOxygenConsumption" ADD CONSTRAINT "DailyOxygenConsumption_bed_id_fkey" FOREIGN KEY ("bed_id") REFERENCES "Bed"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
