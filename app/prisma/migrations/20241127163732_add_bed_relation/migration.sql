/*
  Warnings:

  - You are about to drop the column `department_id` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `last_updated` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `patients_count` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the `IndividualOxygenConsumption` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[bed_id,date]` on the table `DailyOxygenConsumption` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `bed_id` to the `DailyOxygenConsumption` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "DailyOxygenConsumption" DROP CONSTRAINT "DailyOxygenConsumption_department_id_fkey";

-- DropForeignKey
ALTER TABLE "IndividualOxygenConsumption" DROP CONSTRAINT "IndividualOxygenConsumption_daily_oxygen_consumption_id_fkey";

-- DropForeignKey
ALTER TABLE "IndividualOxygenConsumption" DROP CONSTRAINT "IndividualOxygenConsumption_department_id_fkey";

-- DropForeignKey
ALTER TABLE "IndividualOxygenConsumption" DROP CONSTRAINT "IndividualOxygenConsumption_nurse_id_fkey";

-- DropIndex
DROP INDEX "DailyOxygenConsumption_department_id_date_key";

-- Delete existing records
DELETE FROM "DailyOxygenConsumption";

-- Create Bed table first
CREATE TABLE "Bed" (
    "id" TEXT NOT NULL,
    "bed_number" INTEGER NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "department_id" TEXT NOT NULL,

    CONSTRAINT "Bed_pkey" PRIMARY KEY ("id")
);

-- Add foreign key for Bed
ALTER TABLE "Bed" ADD CONSTRAINT "Bed_department_id_fkey" 
    FOREIGN KEY ("department_id") REFERENCES "Department"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- Then proceed with DailyOxygenConsumption changes
ALTER TABLE "DailyOxygenConsumption" ADD "bed_id" TEXT NOT NULL;

-- Add the foreign key constraint
ALTER TABLE "DailyOxygenConsumption" 
ADD CONSTRAINT "DailyOxygenConsumption_bed_id_fkey" 
FOREIGN KEY ("bed_id") REFERENCES "Bed"("id");

-- DropTable
DROP TABLE "IndividualOxygenConsumption";

-- CreateTable
CREATE TABLE "SensorReading" (
    "id" TEXT NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "oxygen_flow" DOUBLE PRECISION NOT NULL,
    "duration" DOUBLE PRECISION NOT NULL,
    "bed_id" TEXT NOT NULL,
    "daily_consumption_id" TEXT NOT NULL,

    CONSTRAINT "SensorReading_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "DailyOxygenConsumption_bed_id_date_key" ON "DailyOxygenConsumption"("bed_id", "date");

-- AddForeignKey
ALTER TABLE "SensorReading" ADD CONSTRAINT "SensorReading_bed_id_fkey" FOREIGN KEY ("bed_id") REFERENCES "Bed"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SensorReading" ADD CONSTRAINT "SensorReading_daily_consumption_id_fkey" FOREIGN KEY ("daily_consumption_id") REFERENCES "DailyOxygenConsumption"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
