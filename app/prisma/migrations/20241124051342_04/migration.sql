-- CreateTable
CREATE TABLE "IndividualOxygenConsumption" (
    "id" SERIAL NOT NULL,
    "departmentId" TEXT NOT NULL,
    "nurseId" TEXT,
    "sensorId" INTEGER,
    "oxygenConsumption" DOUBLE PRECISION NOT NULL,
    "firstTimeUsage" BOOLEAN NOT NULL DEFAULT false,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "remarks" TEXT,

    CONSTRAINT "IndividualOxygenConsumption_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "DailyOxygenConsumption" (
    "id" TEXT NOT NULL,
    "departmentId" TEXT NOT NULL,
    "totalConsumption" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "date" TIMESTAMP(3) NOT NULL DEFAULT (CURRENT_DATE),
    "lastUpdated" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "DailyOxygenConsumption_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "DailyOxygenConsumption_departmentId_date_key" ON "DailyOxygenConsumption"("departmentId", "date");

-- AddForeignKey
ALTER TABLE "IndividualOxygenConsumption" ADD CONSTRAINT "IndividualOxygenConsumption_departmentId_fkey" FOREIGN KEY ("departmentId") REFERENCES "Department"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "IndividualOxygenConsumption" ADD CONSTRAINT "IndividualOxygenConsumption_nurseId_fkey" FOREIGN KEY ("nurseId") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "DailyOxygenConsumption" ADD CONSTRAINT "DailyOxygenConsumption_departmentId_fkey" FOREIGN KEY ("departmentId") REFERENCES "Department"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
