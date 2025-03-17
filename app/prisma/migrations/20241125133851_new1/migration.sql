/*
  Warnings:

  - The primary key for the `IndividualOxygenConsumption` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "DailyOxygenConsumption" ALTER COLUMN "date" SET DEFAULT (CURRENT_DATE);

-- AlterTable
ALTER TABLE "IndividualOxygenConsumption" DROP CONSTRAINT "IndividualOxygenConsumption_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "IndividualOxygenConsumption_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "IndividualOxygenConsumption_id_seq";
