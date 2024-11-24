/*
  Warnings:

  - You are about to drop the column `name` on the `Hospital` table. All the data in the column will be lost.
  - Added the required column `hospital_name` to the `Hospital` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Hospital" DROP COLUMN "name",
ADD COLUMN     "hospital_name" TEXT NOT NULL;
