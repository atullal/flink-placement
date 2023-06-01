package org.apache.flink.runtime.scheduler;

import org.apache.flink.api.common.time.Time;
import org.apache.flink.configuration.CheckpointingOptions;
import org.apache.flink.configuration.ClusterOptions;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.runtime.concurrent.ComponentMainThreadExecutor;
import org.apache.flink.runtime.jobgraph.JobType;
import org.apache.flink.runtime.jobmaster.slotpool.LocationPreferenceSlotSelectionStrategy;
import org.apache.flink.runtime.jobmaster.slotpool.PhysicalSlotProvider;
import org.apache.flink.runtime.jobmaster.slotpool.PhysicalSlotProviderImpl;
import org.apache.flink.runtime.jobmaster.slotpool.PhysicalSlotRequestBulkChecker;
import org.apache.flink.runtime.jobmaster.slotpool.PhysicalSlotRequestBulkCheckerImpl;
import org.apache.flink.runtime.jobmaster.slotpool.PreviousAllocationSlotSelectionStrategy;
import org.apache.flink.runtime.jobmaster.slotpool.SlotPool;
import org.apache.flink.runtime.jobmaster.slotpool.SlotSelectionStrategy;
import org.apache.flink.runtime.scheduler.strategy.PipelinedRegionSchedulingStrategy;
import org.apache.flink.runtime.scheduler.strategy.SchedulingStrategyFactory;
import org.apache.flink.util.clock.SystemClock;

import java.util.function.Consumer;

import static org.apache.flink.util.Preconditions.checkArgument;

/**
 * Components to create a {@link CustomScheduler}. Currently only supports {@link
 * PipelinedRegionSchedulingStrategy}.
 */
public class CustomSchedulerComponents {

    private final SchedulingStrategyFactory schedulingStrategyFactory;
    private final Consumer<ComponentMainThreadExecutor> startUpAction;
    private final ExecutionSlotAllocatorFactory allocatorFactory;

    private CustomSchedulerComponents(
            final SchedulingStrategyFactory schedulingStrategyFactory,
            final Consumer<ComponentMainThreadExecutor> startUpAction,
            final ExecutionSlotAllocatorFactory allocatorFactory) {

        this.schedulingStrategyFactory = schedulingStrategyFactory;
        this.startUpAction = startUpAction;
        this.allocatorFactory = allocatorFactory;
    }

    SchedulingStrategyFactory getSchedulingStrategyFactory() {
        return schedulingStrategyFactory;
    }

    Consumer<ComponentMainThreadExecutor> getStartUpAction() {
        return startUpAction;
    }

    ExecutionSlotAllocatorFactory getAllocatorFactory() {
        return allocatorFactory;
    }

    static CustomSchedulerComponents createSchedulerComponents(
            final JobType jobType,
            final boolean isApproximateLocalRecoveryEnabled,
            final Configuration jobMasterConfiguration,
            final SlotPool slotPool,
            final Time slotRequestTimeout) {

        checkArgument(
                !isApproximateLocalRecoveryEnabled,
                "Approximate local recovery can not be used together with PipelinedRegionScheduler for now! ");
        return createPipelinedRegionSchedulerComponents(
                jobType, jobMasterConfiguration, slotPool, slotRequestTimeout);
    }

    private static CustomSchedulerComponents createPipelinedRegionSchedulerComponents(
            final JobType jobType,
            final Configuration jobMasterConfiguration,
            final SlotPool slotPool,
            final Time slotRequestTimeout) {

        final SlotSelectionStrategy slotSelectionStrategy =
                selectSlotSelectionStrategy(jobMasterConfiguration);
        final PhysicalSlotRequestBulkChecker bulkChecker =
                PhysicalSlotRequestBulkCheckerImpl.createFromSlotPool(
                        slotPool, SystemClock.getInstance());
        final PhysicalSlotProvider physicalSlotProvider =
                new PhysicalSlotProviderImpl(slotSelectionStrategy, slotPool);
        final ExecutionSlotAllocatorFactory allocatorFactory =
                new SlotSharingExecutionSlotAllocatorFactory(
                        physicalSlotProvider,
                        jobType == JobType.STREAMING,
                        bulkChecker,
                        slotRequestTimeout);
        return new CustomSchedulerComponents(
                new PipelinedRegionSchedulingStrategy.Factory(),
                bulkChecker::start,
                allocatorFactory);
    }

    private static SlotSelectionStrategy selectSlotSelectionStrategy(
            final Configuration configuration) {
        final boolean evenlySpreadOutSlots =
                configuration.getBoolean(ClusterOptions.EVENLY_SPREAD_OUT_SLOTS_STRATEGY);

        final SlotSelectionStrategy locationPreferenceSlotSelectionStrategy;

        locationPreferenceSlotSelectionStrategy =
                evenlySpreadOutSlots
                        ? LocationPreferenceSlotSelectionStrategy.createEvenlySpreadOut()
                        : LocationPreferenceSlotSelectionStrategy.createDefault();

        return configuration.getBoolean(CheckpointingOptions.LOCAL_RECOVERY)
                ? PreviousAllocationSlotSelectionStrategy.create(
                        locationPreferenceSlotSelectionStrategy)
                : locationPreferenceSlotSelectionStrategy;
    }
}
