/*
  Warnings:

  - You are about to drop the column `departmentId` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `lastUpdated` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `totalConsumption` on the `DailyOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `bedNumber` on the `IndividualOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `departmentId` on the `IndividualOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `firstTimeUsage` on the `IndividualOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `nurseId` on the `IndividualOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `oxygenConsumption` on the `IndividualOxygenConsumption` table. All the data in the column will be lost.
  - You are about to drop the column `sensorId` on the `IndividualOxygenConsumption` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[department_id,date]` on the table `DailyOxygenConsumption` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `department_id` to the `DailyOxygenConsumption` table without a default value. This is not possible if the table is not empty.
  - Added the required column `bed_number` to the `IndividualOxygenConsumption` table without a default value. This is not possible if the table is not empty.
  - Added the required column `department_id` to the `IndividualOxygenConsumption` table without a default value. This is not possible if the table is not empty.
  - Added the required column `oxygen_consumption` to the `IndividualOxygenConsumption` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "DailyOxygenConsumption" DROP CONSTRAINT "DailyOxygenConsumption_departmentId_fkey";

-- DropForeignKey
ALTER TABLE "IndividualOxygenConsumption" DROP CONSTRAINT "IndividualOxygenConsumption_departmentId_fkey";

-- DropForeignKey
ALTER TABLE "IndividualOxygenConsumption" DROP CONSTRAINT "IndividualOxygenConsumption_nurseId_fkey";

-- DropIndex
DROP INDEX "DailyOxygenConsumption_departmentId_date_key";

-- AlterTable
ALTER TABLE "DailyOxygenConsumption" DROP COLUMN "departmentId",
DROP COLUMN "lastUpdated",
DROP COLUMN "totalConsumption",
ADD COLUMN     "department_id" TEXT NOT NULL,
ADD COLUMN     "last_updated" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "total_consumption" DOUBLE PRECISION NOT NULL DEFAULT 0,
ALTER COLUMN "date" SET DEFAULT (CURRENT_DATE);

-- AlterTable
ALTER TABLE "IndividualOxygenConsumption" DROP COLUMN "bedNumber",
DROP COLUMN "departmentId",
DROP COLUMN "firstTimeUsage",
DROP COLUMN "nurseId",
DROP COLUMN "oxygenConsumption",
DROP COLUMN "sensorId",
ADD COLUMN     "bed_number" INTEGER NOT NULL,
ADD COLUMN     "department_id" TEXT NOT NULL,
ADD COLUMN     "is_first_time_usage" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "nurse_id" TEXT,
ADD COLUMN     "oxygen_consumption" DOUBLE PRECISION NOT NULL,
ADD COLUMN     "sensor_id" INTEGER;

-- CreateIndex
CREATE UNIQUE INDEX "DailyOxygenConsumption_department_id_date_key" ON "DailyOxygenConsumption"("department_id", "date");

-- AddForeignKey
ALTER TABLE "IndividualOxygenConsumption" ADD CONSTRAINT "IndividualOxygenConsumption_department_id_fkey" FOREIGN KEY ("department_id") REFERENCES "Department"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "IndividualOxygenConsumption" ADD CONSTRAINT "IndividualOxygenConsumption_nurse_id_fkey" FOREIGN KEY ("nurse_id") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "DailyOxygenConsumption" ADD CONSTRAINT "DailyOxygenConsumption_department_id_fkey" FOREIGN KEY ("department_id") REFERENCES "Department"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
