import { NativeConnection, Worker } from '@temporalio/worker';
import { powerOf6 } from './activities';

async function run() {
  const temporalAddress = process.env.TEMPORAL_ADDRESS || 'localhost:7233';
  
  // connection to Temporal server
  const connection = await NativeConnection.connect({
    address: temporalAddress,
  });

  // Create worker that hosts the activity
  const worker = await Worker.create({
    connection,
    taskQueue: 'power-of-6-service-queue',
    activities: {
      power_of_6: powerOf6, // Register activity with the name used in workflows
    },
  });

  console.log('Power of 6 worker starting...');
  
  await worker.run();
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});