/*
  Warnings:

  - You are about to drop the column `date` on the `DailyOxygenConsumption` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "DailyOxygenConsumption_bed_id_date_key";

-- AlterTable
ALTER TABLE "DailyOxygenConsumption" DROP COLUMN "date";
