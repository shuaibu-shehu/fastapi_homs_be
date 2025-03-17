/*
  Warnings:

  - Added the required column `bedNumber` to the `IndividualOxygenConsumption` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "DailyOxygenConsumption" ALTER COLUMN "date" SET DEFAULT (CURRENT_DATE);

-- AlterTable
ALTER TABLE "IndividualOxygenConsumption" ADD COLUMN     "bedNumber" INTEGER NOT NULL;
