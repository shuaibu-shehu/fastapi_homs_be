/*
  Warnings:

  - A unique constraint covering the columns `[email]` on the table `Hospital` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "Hospital_email_key" ON "Hospital"("email");
