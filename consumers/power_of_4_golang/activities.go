package main

import (
	"context"
	"os"
	"strconv"
	"time"

	"go.temporal.io/sdk/activity"
)

func PowerOf4(ctx context.Context, a int) (int, error) {
	activityInfo := activity.GetInfo(ctx)
	logger := activity.GetLogger(ctx)

	logger.Info("PowerOf4 activity started", "ActivityID", activityInfo.ActivityID, "input", a)
	waitTimeoutStr := os.Getenv("ACTIVITY_2_WAIT_TIMEOUT")
	waitTimeout, err := strconv.Atoi(waitTimeoutStr)
	if err != nil || waitTimeout == 0 {
		waitTimeout = 5
	}
	time.Sleep(time.Duration(waitTimeout) * time.Second)

	result := a * a * a * a
	logger.Info("PowerOf4 activity completed", "input", a, "result", result)

	return result, nil
}
