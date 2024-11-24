/*
  Warnings:

  - You are about to drop the column `hospital_name` on the `Hospital` table. All the data in the column will be lost.
  - Added the required column `name` to the `Hospital` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Hospital" DROP COLUMN "hospital_name",
ADD COLUMN     "name" TEXT NOT NULL;
