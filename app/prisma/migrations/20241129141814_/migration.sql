/*
  Warnings:

  - A unique constraint covering the columns `[bed_id,date]` on the table `DailyOxygenConsumption` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "DailyOxygenConsumption_bed_id_date_key" ON "DailyOxygenConsumption"("bed_id", "date");
