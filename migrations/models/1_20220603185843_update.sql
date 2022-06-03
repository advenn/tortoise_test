-- upgrade --
ALTER TABLE "user" ALTER COLUMN "user" TYPE VARCHAR(255) USING "user"::VARCHAR(255);
-- downgrade --
ALTER TABLE "user" ALTER COLUMN "user" TYPE UUID USING "user"::UUID;
