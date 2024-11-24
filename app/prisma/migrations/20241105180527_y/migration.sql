/*
  Warnings:

  - You are about to drop the column `phone` on the `Hospital` table. All the data in the column will be lost.
  - Added the required column `contact_person` to the `Hospital` table without a default value. This is not possible if the table is not empty.
  - Added the required column `contact_phone` to the `Hospital` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Hospital" DROP COLUMN "phone",
ADD COLUMN     "contact_person" TEXT NOT NULL,
ADD COLUMN     "contact_phone" TEXT NOT NULL;
