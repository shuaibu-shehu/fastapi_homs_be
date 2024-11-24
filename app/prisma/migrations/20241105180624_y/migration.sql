/*
  Warnings:

  - You are about to drop the column `contact_phone` on the `Hospital` table. All the data in the column will be lost.
  - Added the required column `contact_number` to the `Hospital` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Hospital" DROP COLUMN "contact_phone",
ADD COLUMN     "contact_number" TEXT NOT NULL;
